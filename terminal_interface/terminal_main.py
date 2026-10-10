from math import isqrt

from qqq_backend.qqq_grid import simple_ttt_game


def game_run(simulator):
    grid_size = 9
    result = simple_ttt_game(simulator, grid_size)
    game_state = result
    output_string = ""
    for i in range(1, len(result) + 1):
        if result[i - 1] == 1:
            output_string += 'X'
        else :
            output_string += 'O'
        if i % grid_size == 0:
            output_string += '\n'
    print(logic(result, 2))
    print(output_string)
    
def logic(game_state, winNum):
    board_size = isqrt(len(game_state))
    if board_size * board_size != len(game_state):
        raise ValueError("game_state must contain a square board")
    if not isinstance(winNum, int) or not 1 <= winNum <= board_size:
        raise ValueError("winNum must be between 1 and the board size")
    if any(cell not in (0, 1) for cell in game_state):
        raise ValueError("game_state cells must be 0 or 1")

    directions = ((0, 1), (1, 0), (1, 1), (1, -1))
    for row in range(board_size):
        for column in range(board_size):
            cell = game_state[row * board_size + column]
            for row_step, column_step in directions:
                end_row = row + (winNum - 1) * row_step
                end_column = column + (winNum - 1) * column_step
                if not (
                    0 <= end_row < board_size
                    and 0 <= end_column < board_size
                ):
                    continue

                if all(
                    game_state[
                        (row + step * row_step) * board_size
                        + column
                        + step * column_step
                    ] == cell
                    for step in range(winNum)
                ):
                    return True

    return False