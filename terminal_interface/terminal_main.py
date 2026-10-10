from qqq_backend.qqq_grid import simple_ttt_game
from math import sqrt


def game_run(simulator):
    result = simple_ttt_game(simulator, 3)
    print(result)
    output_string = ""
    for i in range(1, len(result) + 1):
        if result[i - 1] == 1:
            output_string += 'X'
        else :
            output_string += 'O'
        if i % sqrt(len(result)) == 0:
            output_string += '\n'
    print(output_string)
    
def logic():
    pass