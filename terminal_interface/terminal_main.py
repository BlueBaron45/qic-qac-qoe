from qqq_backend import qqq_functions
from qqq_backend.qqq_grid import QQQGrid
from qqq_backend.qqq_block import QQQBlock 

sizeOfGrid = 3

def game_run(simulator):
    grid = QQQGrid(sizeOfGrid)
    found_winner = False
    generator = qqq_functions.set_up_rng_circuit(sizeOfGrid)
    active_player = 'X'
    print_game(grid)
    while not found_winner:
        move_made = False
        while not move_made:
            job = qqq_functions.generate_values_from_rng_circuit(generator, 2, simulator)
            values = qqq_functions.binary_to_decimal(job)
            move_made = grid.make_standard_move(values[0], values[1], active_player)
        found_winner = grid.logic(sizeOfGrid, active_player)
        print("\n" * 4)
        print_game(grid)
        evaulate = measure_grid()
        if evaulate == 'X':
            print(f'winner: {evaulate}')
        elif evaulate == 'Y':
            print(f'winner: {evaulate}')

def print_game(grid:QQQGrid):
    cell_width = 13
    symbol_art = {
        "X": ("X   X", " X X ", "  X  ", " X X ", "X   X"),
        "O": ("  .---.  ", " /     \\ ", "|       |", " \\     / ", "  '---'  "),
        "-": ("     ", "     ", "     ", "     ", "     "),
    }
    rows = grid.get_grid()

    for row_index, row in enumerate(rows):
        rendered_cells = []
        for cell in row:
            state = cell.get_state()
            tilt_x = cell.get_tiltA()
            tilt_o = cell.get_tiltB()
            total_tilts = tilt_x + tilt_o

            if total_tilts > 0:
                chance_x = round(100 * tilt_x / total_tilts)
                chance_o = 100 - chance_x
                chances = f"x:{chance_x:3d}% o:{chance_o:3d}%"
                is_uncertain = tilt_x > 0 and tilt_o > 0
                if not is_uncertain:
                    state = "X" if tilt_x > 0 else "O"
            else:
                chances = "x: --  o: --"
                is_uncertain = False

            if is_uncertain:
                art = ("#" * cell_width,) * 5
            else:
                art = symbol_art.get(state, symbol_art["-"])

            rendered_cells.append(
                [line.center(cell_width) for line in art]
                + [chances.center(cell_width)]
            )

        for line_index in range(6):
            print(" | ".join(cell[line_index] for cell in rendered_cells))

        if row_index < len(rows) - 1:
            print("-+-".join("-" * cell_width for _ in row))

def measure_grid():
    return 'x'
