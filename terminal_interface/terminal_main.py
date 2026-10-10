from qqq_backend import qqq_functions
from qqq_backend.qqq_grid import QQQGrid
from qqq_backend.qqq_block import QQQBlock 


def game_run(simulator):
    grid = QQQGrid(3)
    found_winner = False
    to_win = 3
    generator = qqq_functions.set_up_rng_circuit(3)
    active_player = 'X'
    print_game(grid)
    while not found_winner:
        move_made = False
        while not move_made:
            job = qqq_functions.generate_values_from_rng_circuit(generator, 2, simulator)
            values = qqq_functions.binary_to_decimal(job)
            move_made = grid.make_standard_move(values[0], values[1], active_player)
        found_winner = grid.logic(to_win, simulator)
        print()
        print_game(grid)
        evaulate = measure_grid()
        if evaulate == 'X':
            print(f'winner: {evaulate}')
        elif evaulate == 'Y':
            print(f'winner: {evaulate}')

def print_game(grid:QQQGrid):
    for row in grid.get_grid():
        line = ""
        for cell in row:
            line += str(cell.get_state())
        for cell in row:
            line += " |" +str(cell.get_state())
            line += " X: " + str(cell.tiltA)
            line += " propability of O: " + str(1 - cell.tiltA)
        print(line)

def measure_grid():
    return 'x'
