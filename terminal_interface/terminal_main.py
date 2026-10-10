from math import isqrt

from qqq_backend.qqq_grid import simple_ttt_game


def game_run(simulator, gridSize):
    tiles = ["-", "X", "O"]
    result = simple_ttt_game(simulator, gridSize)
    grid = []
    for i in range(gridSize**2):
        pass
    
    testGrid = [0, 0, 0, 0, " ", " ", 1, 1, " "]
    game_state = result
    output_string = ""
    i = 1
    for tile in testGrid:
        if tile == 1:
            output_string += tiles[1]
        elif tile == 0:
            output_string += tiles[2]
        else:
            output_string += tiles[0]
        if i % gridSize == 0:
            output_string += '\n'
        i += 1
    print(logic(testGrid, 3, 'O'))
    print(output_string)
    
    
def logic(game_state, winNum, character):
    board_size = isqrt(len(game_state))
    if board_size * board_size != len(game_state):
        raise ValueError("game_state must contain a square board")
    if not isinstance(winNum, int) or not 1 <= winNum <= board_size:
        raise ValueError("winNum must be between 1 and the board size")
    if character not in ("X", "O", " "):
        raise ValueError("character must be 'X' or 'O'")
    if any(cell not in (0, 1, " ") for cell in game_state):
        raise ValueError("game_state cells must be 0 or 1")

    target_cell = 1 if character == "X" else 0
    directions = ((0, 1), (1, 0), (1, 1), (1, -1))
    for row in range(board_size):
        for column in range(board_size):
            cell = game_state[row * board_size + column]
            if cell != target_cell:
                continue

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
                    ] == target_cell
                    for step in range(winNum)
                ):
                    return True

    return False

def move(placeOnGrid, gridSize):
    if placeOnGrid >= gridSize-1 or placeOnGrid <= 0:
        ValueError("placeOnGrid must be between: 0-", gridSize-1)
    
    