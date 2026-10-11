"""Entry point for the quantum-inspired tic-tac-toe game.

This file creates the local Aer simulator and launches the board game loop with
configured randomness and quantum mechanics settings.
"""

from qiskit_aer import AerSimulator

from terminal_interface.terminal_main import game_run


# Arguments show up under "Run settings" on Qollab.
# Quantum coin bits = qubits * shots (a game needs roughly 1,500-3,000); 2 more
# qubits form the entangled pair (entangle move) and 4 more run the interference
# tests (wave cells), so the circuit has qubits + 6 qubits in total.
def main(simulator, shots: int = 512, qubits: int = 8, entangle_chance: float = 0.15, wave_chance: float = 0.25):
    """Start a single game session using the provided backend and quantum settings.

    Args:
        simulator: Qiskit backend used to run the initial quantum pool circuit.
        shots: Number of shots per quantum run.
        qubits: Number of coin qubits that drive random decisions.
        entangle_chance: Likelihood an entanglement move is chosen each turn.
        wave_chance: Likelihood a wave action is chosen each turn.
    """
    game_run(simulator, shots, qubits, entangle_chance, wave_chance)


if __name__ == "__main__":
    backend = AerSimulator()
    main(simulator=backend, qubits=4, shots=256, entangle_chance=0.1, wave_chance=0.1)

