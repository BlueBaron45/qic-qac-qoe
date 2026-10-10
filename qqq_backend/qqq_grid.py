from qqq_backend.qqq_block import QQQBlock
from qqq_backend.qqq_functions import generate_parametrized_values_from_circuit
from quantum_evaluators import simple_parametrized_evaluator


class QQQGrid:

    def __init__(self, size: int):
        self.grid = [[QQQBlock() for _ in range(size)] for _ in range(size)]

    def get_grid(self):
        return self.grid

    def make_standard_move(self, x: int, y: int, player) -> bool:
        self.grid[x][y].direct_add(player)

    def logic(self, winNum: int, simulator):
        board_size = len(self.grid)

        if not isinstance(winNum, int) or not 1 <= winNum <= board_size:
            raise ValueError("winNum must be between 1 and the board size")

        directions = (
            (0, 1),  # Horizontal
            (1, 0),  # Vertical
            (1, 1),  # Diagonal down-right
            (1, -1),  # Diagonal down-left
        )

        for row in range(board_size):
            for column in range(board_size):
                spot = self.grid[row][column]
                character = spot.get_state()
                if character == '?':
                    number = generate_parametrized_values_from_circuit(spot.get_tiltA() / (spot.get_tiltA() + spot.get_tiltB()), simulator)
                    if number == 0 :
                        character = 'X'
                    else:
                        character = 'O'
                # Skip empty cells
                if character not in ("X", "O"):
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
                            self.grid[
                                row + step * row_step
                            ][
                                column + step * column_step
                            ].get_state() == character
                            for step in range(winNum)
                    ):
                        return character

        return None