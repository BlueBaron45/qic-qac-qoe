from qiskit_aer import AerSimulator

from terminal_interface.terminal_main import game_run
from quantum_circuit_testing import test_circuit


# Arguments show up under "Run settings" on Qollab.
# Quantum coin bits = qubits * shots (a game needs roughly 1,500-3,000); 2 more
# qubits form the entangled pair (entangle move) and 4 more run the interference
# tests (wave cells), so the circuit has qubits + 6 qubits in total.
def main(simulator, shots: int = 512, qubits: int = 8, entangle_chance: float = 0.15, wave_chance: float = 0.25):
    game_run(backend, shots, qubits, entangle_chance, wave_chance)


if __name__ == "__main__":
    backend = AerSimulator()
    main(simulator=backend)
