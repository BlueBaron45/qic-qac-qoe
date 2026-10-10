from qqq_game_backend import simple_ttt_game


def game_run():
    result = simple_ttt_game()
    output_string = ""
    for i in range(1, len(result) + 1):
        if result[i - 1] == 1:
            output_string += 'X'
        else :
            output_string += 'O'
        if i % 3 == 0:
            output_string += '\n'
    print(output_string)