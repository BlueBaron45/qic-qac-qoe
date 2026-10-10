from qqq_backend import qqq_functions
from qqq_backend.qqq_grid import QQQGrid
from qqq_backend.qqq_block import QQQBlock 

sizeOfGrid = 3

def game_run(simulator):
    grid = QQQGrid(sizeOfGrid)
    found_winner = False
    generator = qqq_functions.set_up_rng_circuit(sizeOfGrid)
    print_game(grid)
    active_player = 'X'
    while not found_winner:
        job = qqq_functions.generate_values_from_rng_circuit(generator, 2, simulator)
        values = qqq_functions.binary_to_decimal(job)
        grid.make_standard_move(values[0], values[1], active_player)
        found_winner = grid.logic(sizeOfGrid, simulator)
        print()
        print_game(grid)
        evaulate = measure_grid()
        if evaulate == 'X':
            print(f'winner: {evaulate}')
        elif evaulate == 'Y':
            print(f'winner: {evaulate}')
        if (active_player == 'X'):
            active_player = 'O'
        else:
            active_player = 'X'

def print_game(grid:QQQGrid):
    for row in grid.get_grid():
        line = ""
        for cell in row:
            line += str(cell.get_state())
        for cell in row:
            line += " |" +str(cell.get_state())
            if cell.get_state() == "-":
                line += "--------"
                line += "--------"
            else:
                line += " |" + str("%") + " X: " + str(1 - cell.tiltA)
                line += " |" + str("%") + " O: " + str(cell.get_tiltA())
        print(line)

def measure_grid():
    return 'x'
