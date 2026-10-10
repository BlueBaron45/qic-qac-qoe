from qqq_backend import qqq_functions
from qqq_backend.qqq_grid import QQQGrid
from qqq_backend.qqq_block import QQQBlock 

sizeOfGrid = 3

def game_run(simulator):
    grid = QQQGrid(sizeOfGrid)
    found_winner = False
    moves_since_measurement = 0
    measurement_interval = 6
    generator = qqq_functions.set_up_rng_circuit(sizeOfGrid)
    print_game(grid)
    active_player = 'X'
    while not found_winner:
        move_made = False
        while not move_made:
            job = qqq_functions.generate_values_from_rng_circuit(generator, 2, simulator)
            values = qqq_functions.binary_to_decimal(job)
            move_made = grid.make_standard_move(values[0], values[1], active_player)
        moves_since_measurement += 1
        if moves_since_measurement == measurement_interval:
            found_winner = grid.logic(sizeOfGrid, simulator)
            moves_since_measurement = 0
        print("\n" * 4)
        print_game(grid)
        if found_winner == 'X':
            print(f'winner: {found_winner}')
        elif found_winner == 'O':
            print(f'winner: {found_winner}')

        if not found_winner:
            active_player = 'O' if active_player == 'X' else 'X'


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
