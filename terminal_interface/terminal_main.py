"""Terminal interface for the quantum tic-tac-toe game."""

import time

from qqq_backend.qqq_pool import QuantumBitPool
from qqq_backend.qqq_grid import QQQGrid


# Game and display settings.
GRID_SIZE = 4
CELL_WIDTH = 15
RANDOM_ROLL_BITS = 8
MEASUREMENT_INTERVAL = 4
MOVE_DELAY_SECONDS = 1


# ASCII art used to display each definite cell state.
SYMBOL_ART = {
    "X": (
        "X   X",
        " X X ",
        "  X  ",
        " X X ",
        "X   X",
    ),
    "O": (
        "  .---.  ",
        " /     \\ ",
        "|       |",
        "|       |",
        " \\     / ",
        "  '---'  ",
    ),
    "-": (
        "     ",
        "     ",
        "     ",
        "     ",
        "     ",
    ),
}


def game_run(
    backend,
    shots: int = 512,
    qubits: int = 8,
    entangle_chance: float = 0.15,
    wave_chance: float = 0.25,
):
    """Run the game until a winning line is found.

    A precomputed QuantumBitPool supplies random values throughout the game,
    so the program does not need to submit a new quantum job for every move.
    Each turn is an entanglement move, a wave operation, or a standard X/O move.
    The board is measured periodically to check for a winner.

    Args:
        backend: Quantum simulator or compatible execution backend.
        shots: Number of shots used to precompute quantum measurement results.
        qubits: Number of random-bit qubits used by QuantumBitPool.
        entangle_chance: Threshold for attempting an entanglement move.
        wave_chance: Additional threshold range for attempting a wave operation.
    """
    move_count = 0
    grid = QQQGrid(GRID_SIZE)
    found_winner = False
    moves_since_measurement = 0
    pool = QuantumBitPool(backend, n_coins=qubits, shots=shots)
    active_player = "X"

    # Show the empty board before the first move.
    print_game(grid)

    while not found_winner:
        # One random value determines which type of move to attempt.
        roll = pool.random(RANDOM_ROLL_BITS)

        # Find cells eligible for each special operation.
        entangle_candidates = grid.entangle_candidates()
        split_candidates = grid.split_candidates()
        wave_cells = grid.wave_cells()

        special_move_made = _try_special_move(
            grid=grid,
            pool=pool,
            player=active_player,
            roll=roll,
            entangle_chance=entangle_chance,
            wave_chance=wave_chance,
            entangle_candidates=entangle_candidates,
            split_candidates=split_candidates,
            wave_cells=wave_cells,
        )

        # If no special operation was performed, place the player's symbol.
        if not special_move_made:
            _make_standard_move(grid, pool, active_player)

        # Measure the board only after the configured number of moves.
        moves_since_measurement += 1
        if moves_since_measurement >= MEASUREMENT_INTERVAL:
            found_winner = grid.logic(GRID_SIZE, pool)
            moves_since_measurement = 0

        # Refresh the terminal display and update the move counter.
        print("\n" * 4)
        print_game(grid)
        move_count += 1
        print(f"Move: {move_count}")

        if found_winner in ("X", "O"):
            print(f"Winner: {found_winner}")
        else:
            # Alternate players only when the game is still in progress.
            active_player = "O" if active_player == "X" else "X"

        time.sleep(MOVE_DELAY_SECONDS)

    # Print diagnostic counters collected by the quantum pool.
    print(
        "Entangled pairs skipped because noise broke the correlation: "
        f"{pool.rejected_pairs}"
    )
    print(
        f"Wave merges: {pool.interference_draws}; "
        "incorrect noisy results in otherwise certain cases: "
        f"{pool.interference_errors}"
    )


def _try_special_move(
    *,
    grid: QQQGrid,
    pool: QuantumBitPool,
    player: str,
    roll: float,
    entangle_chance: float,
    wave_chance: float,
    entangle_candidates: list,
    split_candidates: list,
    wave_cells: list,
) -> bool:
    """Attempt an entanglement or wave operation.

    Return True if a special move was performed; otherwise return False so
    the caller can make a standard X/O move instead.
    """
    # Try to entangle two eligible cells when the roll is in this range.
    if roll < entangle_chance and len(entangle_candidates) >= 2:
        first_cell = entangle_candidates[
            pool.randbelow(len(entangle_candidates))
        ]
        other_candidates = [
            cell for cell in entangle_candidates if cell != first_cell
        ]
        second_cell = other_candidates[pool.randbelow(len(other_candidates))]
        relation = "same" if pool.randbelow(2) == 0 else "opposite"

        grid.make_entangle_move(first_cell, second_cell, relation)
        print(
            f"{player} entangles {first_cell} and {second_cell}: "
            f"they will measure as {relation}"
        )
        return True

    # The wave range starts after the entanglement threshold. If entanglement
    # was unavailable, this branch can also be reached for a low roll.
    if roll < entangle_chance + wave_chance and (split_candidates or wave_cells):
        # If a wave already exists, either shift its phase or merge it.
        # Otherwise, split a definite X/O cell to create the first wave.
        actions = ["phase", "merge"] if wave_cells else ["split"]
        action = actions[pool.randbelow(len(actions))]

        if action == "split":
            cell = split_candidates[pool.randbelow(len(split_candidates))]
            original_symbol = grid.get_grid()[cell[0]][cell[1]].get_state()
            grid.make_split_move(cell)
            print(
                f"{player} splits {cell} (was {original_symbol}) into a wave: H gate"
            )

        elif action == "phase":
            cell = wave_cells[pool.randbelow(len(wave_cells))]
            grid.add_phase(cell)
            print(f"{player} adds a hidden phase shift to the wave at {cell}: S gate")

        else:  # action == "merge"
            cell = wave_cells[pool.randbelow(len(wave_cells))]
            symbol, phase = grid.merge_wave(cell, pool)
            print(
                f"{player} merges the wave at {cell} (H gate): it had "
                f"{phase} phase shift(s) mod 4 and becomes {symbol}"
            )

        return True

    return False


def _make_standard_move(grid: QQQGrid, pool: QuantumBitPool, player: str) -> None:
    """Choose random coordinates until a standard move is accepted."""
    move_made = False

    while not move_made:
        row = pool.randbelow(GRID_SIZE)
        column = pool.randbelow(GRID_SIZE)
        move_made = grid.make_standard_move(row, column, player)


def print_game(grid: QQQGrid) -> None:
    """Print the board, showing each cell's symbol and estimated probabilities."""
    rows = grid.get_grid()

    for row_index, row in enumerate(rows):
        rendered_cells = []

        for cell in row:
            # Read the current cell state and its X/O contribution counters.
            state = cell.get_state()
            tilt_x = cell.get_tiltA()
            tilt_o = cell.get_tiltB()
            total_tilts = tilt_x + tilt_o

            # Estimate the displayed X/O probabilities from the cell counters.
            if total_tilts > 0:
                is_uncertain = state == "?"

                if is_uncertain:
                    chance_x = round(100 * tilt_x / total_tilts)
                    chance_o = 100 - chance_x
                else:
                    chance_x = 100 if state == "X" else 0
                    chance_o = 100 - chance_x

                probabilities = (
                    f"X: {chance_x:3d}%",
                    f"O: {chance_o:3d}%",
                )
            else:
                # Untouched cells have no contributions, so show placeholders.
                probabilities = ("X:  --", "O:  --")
                is_uncertain = False

            # Choose the ASCII art for a definite symbol or an uncertain cell.
            if is_uncertain:
                art = ("#" * CELL_WIDTH,) * 6

                if cell.is_wave():
                    label = f" wave (was {cell.wave_origin}) "
                    art = art[:2] + (label.center(CELL_WIDTH, "#"),) + art[3:]

                if cell.is_entangled():
                    relation_symbol = "=" if cell.relation == "same" else "!="
                    label = f" pair {cell.tag} ({relation_symbol}) "
                    art = art[:2] + (label.center(CELL_WIDTH, "#"),) + art[3:]
            else:
                art = SYMBOL_ART.get(state, SYMBOL_ART["-"])

            # Give every cell six art lines before adding the two probability lines.
            art = art + ("",) * (6 - len(art))
            rendered_cells.append(
                [line.center(CELL_WIDTH) for line in art]
                + [line.center(CELL_WIDTH) for line in probabilities]
            )

        # Print the cells one line at a time so their ASCII art stays aligned.
        cell_height = max(len(cell_lines) for cell_lines in rendered_cells)
        for line_index in range(cell_height):
            print(" | ".join(cell_lines[line_index] for cell_lines in rendered_cells))

        # Separate board rows with a horizontal divider, except after the last row.
        if row_index < len(rows) - 1:
            print("-+-".join("-" * CELL_WIDTH for _ in row))
