from qqq_backend.qqq_pool import QuantumBitPool
from qqq_backend.qqq_grid import QQQGrid
from qqq_backend.qqq_block import QQQBlock 
from quantum_circuit_testing import test_circuit

sizeOfGrid = 3


def game_run(backend, shots: int = 512, qubits: int = 8, entangle_chance: float = 0.15,
             wave_chance: float = 0.25):
    """Run the quantum tic-tac-toe game until a winner is found.

    Each turn uses the quantum pool to choose between an entanglement move,
    a wave operation, or a standard X/O move. The board is measured every
    few moves to check for a winner, then displayed along with move and
    noise statistics.
    """
    move_count = 0
    grid = QQQGrid(sizeOfGrid)
    shownGrid = QQQGrid(sizeOfGrid)
    found_winner = False
    moves_since_measurement = 0
    measurement_interval = 4
    pool = QuantumBitPool(backend, n_coins=qubits, shots=shots)  # the ONE quantum job
    #test_circuit(backend, circuit=pool.getCiruit())
    print_game(grid)
    active_player = 'X'
    while not found_winner:
        # one quantum number decides what kind of move this turn is
        roll = pool.random(8)
        candidates = grid.entangle_candidates()
        splits, waves = grid.split_candidates(), grid.wave_cells()
        if roll < entangle_chance and len(candidates) >= 2:
            a = candidates[pool.randbelow(len(candidates))]
            others = [c for c in candidates if c != a]
            b = others[pool.randbelow(len(others))]
            relation = 'same' if pool.randbelow(2) == 0 else 'opposite'
            grid.make_entangle_move(a, b, relation)
            print(f"{active_player} entangles {a} and {b}: they will measure as {relation}")
        elif roll < entangle_chance + wave_chance and (splits or waves):
            # while a wave exists, play with it; otherwise create one
            options = ['phase', 'merge'] if waves else ['split']
            action = options[pool.randbelow(len(options))]
            if action == 'split':
                cell = splits[pool.randbelow(len(splits))]
                was = grid.get_grid()[cell[0]][cell[1]].get_state()
                grid.make_split_move(cell)
                print(f"{active_player} splits {cell} (was {was}) into a wave: H gate")
            elif action == 'phase':
                cell = waves[pool.randbelow(len(waves))]
                grid.add_phase(cell)
                print(f"{active_player} adds a hidden phase shift to the wave at {cell}: S gate")
            else:
                cell = waves[pool.randbelow(len(waves))]
                symbol, k = grid.merge_wave(cell, pool)
                print(f"{active_player} merges the wave at {cell} (H gate): it had {k} phase "
                      f"shift(s) mod 4 and becomes {symbol}")
        else:
            move_made = False
            while not move_made:
                x = pool.randbelow(sizeOfGrid)
                y = pool.randbelow(sizeOfGrid)
                move_made = grid.make_standard_move(x, y, active_player)
        moves_since_measurement += 1
        if moves_since_measurement == measurement_interval:
            found_winner = grid.logic(sizeOfGrid, pool)
            moves_since_measurement = 0
        print("\n" * 4)
        print_game(grid)
        move_count +=1
        print("move: ", move_count)
        if found_winner == 'X':
            print(f'winner: {found_winner}')
        elif found_winner == 'O':
            print(f'winner: {found_winner}')

        if not found_winner:
            active_player = 'O' if active_player == 'X' else 'X'
        else:
            print(f"entangled pairs skipped because noise broke the correlation: "
                  f"{pool.rejected_pairs}")
            print(f"wave merges: {pool.interference_draws}, "
                  f"wrong results from noise on the certain cases: {pool.interference_errors}")


def print_game(grid: QQQGrid):
    # 1. Define visual formatting settings and ASCII art for each symbol
    cell_width = 15
    symbol_art = {
        "X": ("X   X",
              " X X ",
              "  X  "
            ," X X ",
              "X   X"),
        "O": (
            "  .---.  ",
            " /     \\ ",
            "|       |",
            "|       |",
            " \\     / ",
            "  '---'  ",
        ),
        "-": ("     ", 
              "     ", 
              "     ",
              "     "
            , "     "),
    }
    
    # Retrieve the 2D grid structure containing all cells
    rows = grid.get_grid()

    # 2. Iterate through each row in the grid
    for row_index, row in enumerate(rows):
        rendered_cells = []
        
        # Process every individual cell in the current row
        for cell in row:
            # Get current cell properties (state and quantum tilt values for X and O)
            state = cell.get_state()
            tilt_x = cell.get_tiltA()
            tilt_o = cell.get_tiltB()
            total_tilts = tilt_x + tilt_o

            # --- Calculate Probabilities ---
            if total_tilts > 0:
                is_uncertain = state == '?'
                if is_uncertain:
                    chance_x = round(100 * tilt_x / total_tilts)
                    chance_o = 100 - chance_x
                else:
                    chance_x = 100 if state == "X" else 0
                    chance_o = 100 - chance_x

                chances = (
                    f"X: {chance_x:3d}%",
                    f"O: {chance_o:3d}%",
                )
            else:
                # Default probabilities for an untouched/empty cell
                chances = ("X:  --", "O:  --")
                is_uncertain = False

            # --- Select ASCII Art Representation ---
            if is_uncertain:
                # Block out the cell with '#' symbols to represent an uncertain/superposition state
                art = ("#" * cell_width,) * 6
                if cell.is_wave():
                    label = f" wave (was {cell.wave_origin}) "
                    art = art[:2] + (label.center(cell_width, '#'),) + art[3:]
                if cell.is_entangled():
                    sign = '=' if cell.relation == 'same' else '!='
                    label = f" pair {cell.tag} ({sign}) "
                    art = art[:2] + (label.center(cell_width, '#'),) + art[3:]
            else:
                # Pick corresponding ASCII art for 'X', 'O', or empty '-'
                art = symbol_art.get(state, symbol_art["-"])
            
            # Pad the art tuple to ensure it has at least 6 lines
            art = art + ("",) * (6 - len(art))

            # Combine centered ASCII art lines with centered probability text lines for this cell
            rendered_cells.append(
                [line.center(cell_width) for line in art]
                + [line.center(cell_width) for line in chances]
            )

        # --- Render and Print Grid Line-by-Line ---
        # Find max total lines needed to draw a single cell vertically
        cell_height = max(len(cell) for cell in rendered_cells)
        
        # Print the row line by line across all cells, separated by vertical bars '|'
        for line_index in range(cell_height):
            print(" | ".join(cell[line_index] for cell in rendered_cells))

        # Print horizontal dividers ('-+-') between grid rows (except after the last row)
        if row_index < len(rows) - 1:
            print("-+-".join("-" * cell_width for _ in row))
