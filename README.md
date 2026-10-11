# Quantum QQQ

A small experimental Python project that turns a classic tic-tac-toe board into a quantum-inspired game. The game uses a single compiled Qiskit circuit to generate random coin flips, Bell-pair correlations, and interference-based wave effects, then applies those quantum outcomes to a 3x3 board.

This repo is a prototype for exploring how quantum randomness, entanglement, and phase interference can influence a turn-based board game. It is built with Qiskit and runs locally with the Aer simulator by default.

## Project overview

The project blends three ideas:

- Quantum coin tosses determine random moves and probabilities
- Entangled cells link two board positions so they measure consistently
- Wave cells split, phase-shift, and merge using interference behavior

The game loop is implemented in [terminal_interface/terminal_main.py](terminal_interface/terminal_main.py), while the underlying board logic and quantum resource pool live in [qqq_backend](qqq_backend).

## Features

- 3x3 quantum tic-tac-toe board
- Standard X/O placements on empty cells
- Entanglement move between two valid empty or uncertain cells
- Split/merge wave mechanic using hidden phase states
- Randomized board measurement with quantum probability display
- Local simulation using Qiskit Aer
- Debug/testing utilities for quantum circuits and histogram inspection

## Repository structure

- [main.py](main.py) — entry point; creates the simulator and starts the game
- [terminal_interface/terminal_main.py](terminal_interface/terminal_main.py) — main game loop and ASCII board renderer
- [qqq_backend/qqq_pool.py](qqq_backend/qqq_pool.py) — quantum bit pool and random-source abstraction
- [qqq_backend/qqq_grid.py](qqq_backend/qqq_grid.py) — board mechanics, winning logic, entanglement, and wave rules
- [qqq_backend/qqq_block.py](qqq_backend/qqq_block.py) — cell state and quantum tilt tracking
- [quantum_circuit_testing.py](quantum_circuit_testing.py) — helper utilities for circuit testing and visualization
- [obsolete](obsolete) — older, experimental code not used by the active game

## How the game works

The game creates one quantum circuit that contains:

1. Coin qubits for fair random numbers
2. Bell-pair qubits for entanglement between cells
3. Interference qubits for wave/phase operations

Each turn, the game draws from that generated quantum pool:

- Random value decides whether to place a move, split a wave, or entangle cells
- Entangled cells are linked and later resolve into consistent X/O outcomes
- Wave cells can be split into a superposition, phase-shifted, and merged back into a definite symbol
- Board checks run periodically and winners are detected using the standard aligned-line logic

The turn-by-turn visual output prints an ASCII board along with per-cell probability estimates for X and O.

## Installation

The project is Python-based and requires Qiskit dependencies.

```bash
python -m venv .venv
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
# Linux/macOS
# source .venv/bin/activate

pip install qiskit qiskit-aer
```

## Run the game

From the project root:

```bash
python main.py
```

The default script starts the simulator and runs the game with:

- 4 qubits
- 256 shots
- 10% entanglement chance
- 10% wave chance

These values are defined in [main.py](main.py) and can be adjusted directly.

## Main configuration

The entry point exposes a function that accepts simulator, shots, qubits, entangle_chance, and wave_chance:

```python
main(simulator=backend, qubits=4, shots=256, entangle_chance=0.1, wave_chance=0.1)
```

You can tweak these parameters to change the game behavior and the volume of quantum randomness generated per run.

## Notes on the implementation

This is an experimental amusement project rather than a polished game engine. Some parts of the code intentionally model quantum behavior with simplified rules and statistical outcomes rather than exact, fully hardware-faithful semantics.

The core mechanics are:

- `QuantumBitPool` creates a reusable quantum source for random decisions
- `QQQGrid` manages board state and move validation
- `QQQBlock` tracks each cell's state, tilt, entanglement, and wave metadata

## Troubleshooting

- If Qiskit imports fail, reinstall the required dependencies with `pip install qiskit qiskit-aer`
- If the game exits early, confirm the simulator backend is available and that the environment is using the intended Python interpreter
- For circuit testing and experimentation, use the helper functions in [quantum_circuit_testing.py](quantum_circuit_testing.py)

## License

This project does not currently declare a formal license file. Check the repository settings or upstream project context before redistribution or reuse.
