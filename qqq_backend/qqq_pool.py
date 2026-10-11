"""Quantum random bit pool for Qollab.

Qollab (IonQ) allows ONE circuit job per run, so we run a single circuit once
and hand the measured results out during the game. Every shot contains

  * n_coins qubits: H + measure          -> fair quantum coins (random numbers)
  * bell_pairs pairs of qubits: H, CNOT  -> entangled pairs (|00> + |11>)/sqrt(2)
                                            used by the "entangle two cells" move
  * 4 interference qubits, one per number of phase shifts k = 0..3:
        H - barrier - S^k - barrier - H - measure
    Probability of reading 0 is cos^2(k*pi/4): always 0 (k=0), 50% (k=1),
    always 1 (k=2), 50% (k=3). Used by the wave-cell "merge" move.
"""
import random
from qiskit import QuantumCircuit, transpile


def generate_bit_pool_circuit(n_coins: int = 8, shots: int = 512, bell_pairs: int = 1):
    """Build the one-shot quantum circuit used to seed the game with randomness.

    The circuit creates a reusable pool of random coin bits, Bell pairs, and
    interference measurements. The caller can then consume those values across a
    full game without submitting a new backend job.
    """
    base = n_coins + 2 * bell_pairs  # first interference qubit
    n = base + 4
    qc = QuantumCircuit(n, n)
    qc.h(range(n_coins))
    for k in range(bell_pairs):
        a = n_coins + 2 * k
        qc.h(a)
        qc.cx(a, a + 1)  # entangle qubit a with a + 1
    for k in range(4):
        q = base + k
        qc.h(q)
        qc.barrier(q)  # stop the compiler cancelling H...H
        if k == 1:
            qc.s(q)  # +90 degrees of phase
        elif k == 2:
            qc.z(q)  # 180 degrees (= two S gates)
        elif k == 3:
            qc.sdg(q)  # 270 degrees (= three S gates)
        qc.barrier(q)
        qc.h(q)
    qc.measure(range(n), range(n))
    return qc


class QuantumBitPool:
    """Store one quantum job and expose random values to the game engine.

    The pool is the bridge between Qiskit hardware/simulation and board logic.
    It records fair random coin bits, Bell-pair outcomes for entanglement, and
    interference results used by wave mechanics. Each method consumes a chunk of
    precomputed quantum data so the game can act like a random source without
    submitting a second circuit.
    """

    def __init__(self, backend, n_coins: int = 8, shots: int = 512, bell_pairs: int = 1):
        """Compile a single circuit, execute it once, and unpack the results.

        Args:
            backend: Qiskit simulator/backend used for execution.
            n_coins: Number of fair random coin qubits.
            shots: Number of measurement shots per circuit execution.
            bell_pairs: Number of Bell pairs to create for entanglement actions.
        """
        base = n_coins + 2 * bell_pairs          # first interference qubit
        n = base + 4
        self.qc = QuantumCircuit(n, n)
        self.qc.h(range(n_coins))
        for k in range(bell_pairs):
            a = n_coins + 2 * k
            self.qc.h(a)
            self.qc.cx(a, a + 1)                      # entangle qubit a with a + 1
        for k in range(4):
            q = base + k
            self.qc.h(q)
            self.qc.barrier(q)                        # stop the compiler cancelling H...H
            if k == 1:
                self.qc.s(q)                          # +90 degrees of phase
            elif k == 2:
                self.qc.z(q)                          # 180 degrees (= two S gates)
            elif k == 3:
                self.qc.sdg(q)                        # 270 degrees (= three S gates)
            self.qc.barrier(q)
            self.qc.h(q)
        self.qc.measure(range(n), range(n))

        self.qc = transpile(self.qc, backend, optimization_level=3)
        result = backend.run(self.qc, shots=shots, memory=True).result()
        try:
            words = result.get_memory()          # one bitstring per shot, in order
        except Exception:
            # Backend gives only counts: rebuild the shots and put them in random order
            words = [w for w, c in result.get_counts().items() for _ in range(c)]
            random.shuffle(words)

        coins, pairs = [], []
        self.interference = {k: [] for k in range(4)}
        for w in words:
            bits = w.replace(" ", "")[::-1]      # Qiskit prints qubit 0 on the right
            coins.append(bits[:n_coins])
            for k in range(bell_pairs):
                a = n_coins + 2 * k
                pairs.append((bits[a], bits[a + 1]))
            for k in range(4):
                self.interference[k].append(int(bits[base + k]))
        self.bits = "".join(coins)
        self.pos = 0
        self.pairs = pairs
        self.pair_pos = 0
        self.rejected_pairs = 0                  # pairs whose two qubits disagreed (noise)
        self.interference_pos = {k: 0 for k in range(4)}
        self.interference_draws = 0
        self.interference_errors = 0             # k=0 / k=2 results that broke the ideal answer
        print(f"Quantum pool ready: {len(self.bits)} coin bits, {len(self.pairs)} "
              f"entangled pairs and {len(words)} interference runs from {backend} ({n} qubits)")

    def getCiruit(self):
        """Return the compiled quantum circuit used to generate the pool."""
        return self.qc

    # ---- plain random numbers -------------------------------------------------
    def _take(self, k: int) -> int:
        """Consume k bits from the pre-generated pool and return them as an integer."""
        if self.pos + k > len(self.bits):
            raise RuntimeError("Out of quantum bits - raise 'shots' in main()")
        chunk = self.bits[self.pos:self.pos + k]
        self.pos += k
        return int(chunk, 2)

    def randbelow(self, n: int) -> int:
        """Return a uniformly random integer in the range [0, n)."""
        k = max(1, (n - 1).bit_length())
        while True:
            value = self._take(k)
            if value < n:
                return value

    def random(self, k: int = 16) -> float:
        """Return a floating-point random value in the inclusive/exclusive range [0, 1)."""
        return self._take(k) / (1 << k)

    # ---- entangled pairs ----------------------------------------------------------
    def bell_pair(self) -> int:
        """Return a valid Bell-pair measurement if the noisy pair still agrees.

        The method skips mismatched pairs and counts them as rejected. This models
        the fact that real hardware can break perfect long-range correlation.
        """
        while self.pair_pos < len(self.pairs):
            a, b = self.pairs[self.pair_pos]
            self.pair_pos += 1
            if a == b:
                return int(a)
            self.rejected_pairs += 1
        raise RuntimeError("Out of entangled pairs - raise 'shots' in main()")

    # ---- interference ---------------------------------------------------------------
    def interference_bit(self, k: int) -> int:
        """Return the outcome of a phase-shifted interference experiment.

        The value is the measured bit after H-S^k-H. For k=0 and k=2 it should be
        deterministic; for k=1 and k=3 it is a 50/50 draw. When hardware noise
        changes a previously certain outcome, the error counter is incremented.
        """
        k %= 4
        pos = self.interference_pos[k]
        if pos >= len(self.interference[k]):
            raise RuntimeError("Out of interference results - raise 'shots' in main()")
        self.interference_pos[k] += 1
        bit = self.interference[k][pos]
        self.interference_draws += 1
        if (k == 0 and bit == 1) or (k == 2 and bit == 0):
            self.interference_errors += 1
        return bit
    