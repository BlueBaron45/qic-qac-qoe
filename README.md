# Quantum QQQ

Quantum QQQ is a small experimental terminal game that blends classic board-play with quantum-inspired mechanics. The project uses a single Qiskit circuit to generate reusable random coin bits, Bell-pair correlations, and phase-interference outcomes, then applies those results to a game board.

This repository is a local prototype and is intentionally lightweight: it runs from the terminal, uses Qiskit Aer for simulation, and focuses on exploring how randomness, entanglement, and wave interference can affect turns and outcomes in a board game.

## What the project does

The game creates a 4x4 board and each turn can do one of three things:

- place a standard X/O move on an empty cell
- entangle two valid cells so they resolve together as a correlated pair
- split, phase-shift, and merge a wave cell to simulate interference behavior

The board is measured periodically, and the game checks for a winner using the current board rules in [qqq_backend/qqq_grid.py](qqq_backend/qqq_grid.py).

## Current implementation

The active code is centered around these files:

- [main.py](main.py) — program entry point; creates the Aer simulator and starts a single game session
- [terminal_interface/terminal_main.py](terminal_interface/terminal_main.py) — game loop, random move selection, ASCII rendering, and board measurement flow
- [qqq_backend/qqq_pool.py](qqq_backend/qqq_pool.py) — builds the quantum circuit once, stores measured results, and exposes random/entangled/interference values to the game
- [qqq_backend/qqq_grid.py](qqq_backend/qqq_grid.py) — board state, move validation, entanglement rules, wave mechanics, and win detection
- [qqq_backend/qqq_block.py](qqq_backend/qqq_block.py) — per-cell state and quantum metadata such as tilt, pair tags, and wave phase
- [quantum_circuit_testing.py](quantum_circuit_testing.py) — debugging utilities for circuit inspection and experiments
- [obsolete](obsolete) — older prototype code kept out of the current runtime path

## Game rules and behavior

The current terminal version uses a 4x4 grid rather than a classic 3x3 board. The game flow in [terminal_interface/terminal_main.py](terminal_interface/terminal_main.py) is:

1. create a single `QuantumBitPool` from one Qiskit circuit
2. choose a random move type each tick
3. apply a special move when eligible, otherwise place a standard move
4. measure the board every 4 turns
5. continue until a winning line is found

The quantum pool includes:

- fair coin bits for random move selection and probability estimates
- Bell-pair data for entangled-cell relationships
- 4 interference outcomes used by wave-cell merges

The board prints an ASCII layout and shows estimated X/O probabilities for each cell, so the terminal output reveals the quantum-inspired state even before a cell resolves definitively.

## Installation

This project is Python-based and uses Qiskit plus the Aer simulator.

```bash
python -m venv .venv
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
# macOS/Linux
# source .venv/bin/activate

pip install qiskit qiskit-aer
```

## Run the game

From the repository root:

```bash
python main.py
```

The default configuration in [main.py](main.py) is:

```python
backend = AerSimulator()
main(
    backend,
    shots=512,
    qubits=2,
    entangle_chance=0.1,
    wave_chance=0.1,
)
```

That means the game currently starts with:

- 512 shots per quantum run
- 2 coin qubits for the random source
- 10% entanglement chance per turn window
- 10% wave chance per turn window

The terminal loop also fixes the board size to 4 and checks for a result every 4 moves.

## Configuration notes

The `main()` function accepts the simulator, shot count, coin qubit count, entanglement chance, and wave chance. These parameters can be adjusted directly in [main.py](main.py) to change the behavior and randomness profile of a run.

## Project status

This repository is best understood as a research-style game prototype rather than a packaged application. It focuses on experimentation and local simulation, and some parts of the implementation intentionally model quantum ideas with simplified statistical behavior instead of exact hardware-level semantics.

## Troubleshooting

- If Qiskit import errors appear, reinstall the required packages with `pip install qiskit qiskit-aer`.
- If the game exits early, confirm that the selected Python environment has both `qiskit` and `qiskit-aer` available.
- For circuit-level experimentation, inspect [quantum_circuit_testing.py](quantum_circuit_testing.py) and the logic in [qqq_backend/qqq_pool.py](qqq_backend/qqq_pool.py).

## License

This repository does not currently include a formal license file. If you plan to redistribute or reuse the code, confirm the licensing expectations with the project owner or repository context before doing so.
