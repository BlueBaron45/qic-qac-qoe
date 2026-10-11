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
from qiskit import QuantumCircuit

def generate_bit_pool_circuit(n_coins: int = 8, shots: int = 512, bell_pairs: int = 1):
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
    def __init__(self, backend, n_coins: int = 8, shots: int = 512, bell_pairs: int = 1):
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
       return self.qc
    

    # ---- plain random numbers -------------------------------------------------
    def _take(self, k: int) -> int:
        if self.pos + k > len(self.bits):
            raise RuntimeError("Out of quantum bits - raise 'shots' in main()")
        chunk = self.bits[self.pos:self.pos + k]
        self.pos += k
        return int(chunk, 2)

    def randbelow(self, n: int) -> int:
        """Uniform integer 0..n-1 (rejection sampling keeps it fair)."""
        k = max(1, (n - 1).bit_length())
        while True:
            value = self._take(k)
            if value < n:
                return value

    def random(self, k: int = 16) -> float:
        """Uniform float in [0, 1) with k bits of resolution."""
        return self._take(k) / (1 << k)

    # ---- entangled pairs ----------------------------------------------------------
    def bell_pair(self) -> int:
        """Measure one entangled pair and return the bit both qubits agree on.
        On real hardware noise sometimes breaks the correlation; those pairs are
        skipped and counted in rejected_pairs."""
        while self.pair_pos < len(self.pairs):
            a, b = self.pairs[self.pair_pos]
            self.pair_pos += 1
            if a == b:
                return int(a)
            self.rejected_pairs += 1
        raise RuntimeError("Out of entangled pairs - raise 'shots' in main()")

    # ---- interference ---------------------------------------------------------------
    def interference_bit(self, k: int) -> int:
        """Result of H - S^k - H on a fresh qubit: 0 means it returned to its start.
        Ideal: k=0 -> 0, k=2 -> 1, k=1 or 3 -> 50/50. On hardware, noise can break
        the two certain cases; those are counted in interference_errors."""
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
    