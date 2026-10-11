from qiskit_aer import AerSimulator

from terminal_interface.terminal_main import game_run


# Arguments show up under "Run settings" on Qollab.
# Quantum coin bits = qubits * shots (a game needs roughly 1,500-3,000); 2 more
# qubits form the entangled pair (entangle move) and 4 more run the interference
# tests (wave cells), so the circuit has qubits + 6 qubits in total.
def main(simulator, shots, qubits: int, entangle_chance: float , wave_chance: float ):
    game_run(simulator, shots, qubits, entangle_chance, wave_chance)


if __name__ == "__main__":
    backend = AerSimulator()
    main(backend, shots=192, qubits=2, entangle_chance=0.1, wave_chance=0.1)
