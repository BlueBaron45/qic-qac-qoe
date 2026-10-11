from qqq_backend.qqq_block import QQQBlock


class QQQGrid:
    """Represent the full game board and handle all board-state rules.

    This class stores the 2D cell grid, validates legal moves, applies the
    quantum-style special actions (entanglement and wave mechanics), and checks
    whether a winning line has been formed after a measurement round.
    """

    def __init__(self, size: int):
        """Create a square board with one QQQBlock instance per cell."""
        self.grid = [[QQQBlock() for _ in range(size)] for _ in range(size)]
        self.pair_count = 0

    def get_grid(self):
        """Return the board matrix so other parts of the program can render or inspect it."""
        return self.grid

    def make_standard_move(self, x: int, y: int, player) -> bool:
        """Place a normal X/O move on a cell unless it is locked by quantum rules."""
        if self.grid[x][y].is_entangled() or self.grid[x][y].is_wave():
            return False
        self.grid[x][y].direct_add(player)
        return True

    def unlocked_cells(self):
        """Cells a normal move may use (not entangled, not a wave)."""
        return [(r, c) for r in range(len(self.grid)) for c in range(len(self.grid))
                if not self.grid[r][c].is_entangled() and not self.grid[r][c].is_wave()]

    def can_entangle(self, a, b) -> bool:
        """Check whether two positions are valid targets for a Bell-pair entanglement move."""
        if a == b:
            return False
        for row, column in (a, b):
            cell = self.grid[row][column]
            if cell.is_entangled() or cell.is_wave() or cell.get_state() in ('X', 'O'):
                return False
        return True

    def entangle_candidates(self):
        """Return all cells currently eligible to become part of an entanglement pair."""
        return [
            (row, column)
            for row in range(len(self.grid))
            for column in range(len(self.grid))
            if not self.grid[row][column].is_entangled()
            and not self.grid[row][column].is_wave()
            and self.grid[row][column].get_state() in ('-', '?')
        ]

    def make_entangle_move(self, a, b, relation: str) -> bool:
        """Link two cells so they will resolve together as a correlated quantum pair."""
        if relation not in ('same', 'opposite') or not self.can_entangle(a, b):
            return False
        tag = chr(ord('a') + self.pair_count % 26)
        self.pair_count += 1
        for mine, other in ((a, b), (b, a)):
            cell = self.grid[mine[0]][mine[1]]
            cell.partner, cell.relation, cell.tag = other, relation, tag
            cell.set_tiltA(1)
            cell.set_tiltB(1)
            cell.set_state('?')
        return True

    @staticmethod
    def _make_definite(block, symbol):
        """Turn a quantum-style uncertain cell into a definite X/O cell and clear its quantum metadata."""
        block.set_state(symbol)
        block.set_tiltA(1 if symbol == 'X' else 0)
        block.set_tiltB(1 if symbol == 'O' else 0)
        block.partner = block.relation = block.tag = None
        block.wave_origin = None
        block.wave_phase = 0

    def wave_cells(self):
        """Return every cell currently in the wave/interference state."""
        return [(r, c) for r in range(len(self.grid)) for c in range(len(self.grid))
                if self.grid[r][c].is_wave()]

    def split_candidates(self):
        """Return definite cells that can be converted into a wave state."""
        return [(r, c) for r in range(len(self.grid)) for c in range(len(self.grid))
                if self.grid[r][c].get_state() in ('X', 'O')
                and not self.grid[r][c].is_entangled()
                and not self.grid[r][c].is_wave()]

    def make_split_move(self, a) -> bool:
        """Split a definite cell into a wave state to simulate an H-gate transformation."""
        if a not in self.split_candidates():
            return False
        cell = self.grid[a[0]][a[1]]
        cell.wave_origin = cell.get_state()
        cell.wave_phase = 0
        cell.set_tiltA(1)
        cell.set_tiltB(1)
        cell.set_state('?')
        return True

    def add_phase(self, a) -> bool:
        """Increase the hidden phase offset on an existing wave cell."""
        cell = self.grid[a[0]][a[1]]
        if not cell.is_wave():
            return False
        cell.wave_phase += 1
        return True

    def merge_wave(self, a, pool):
        """Resolve a wave state through interference and convert it back into a definite X/O result."""
        cell = self.grid[a[0]][a[1]]
        k = cell.wave_phase % 4
        bit = pool.interference_bit(k)
        origin = cell.wave_origin
        symbol = origin if bit == 0 else ('O' if origin == 'X' else 'X')
        self._make_definite(cell, symbol)
        return symbol, k

    def _measure_pair(self, cell, pool):
        """Measure an entangled pair and assign final X/O values to both linked cells."""
        partner = self.grid[cell.partner[0]][cell.partner[1]]
        bit = pool.bell_pair()
        first = 'X' if bit == 0 else 'O'
        flipped = 'O' if first == 'X' else 'X'
        second = first if cell.relation == 'same' else flipped
        for block, symbol in ((cell, first), (partner, second)):
            self._make_definite(block, symbol)

    def logic(self, winNum: int, pool):
        """Resolve uncertain cells and return the winning symbol if a line is formed."""
        board_size = len(self.grid)

        if not isinstance(winNum, int) or not 1 <= winNum <= board_size:
            raise ValueError("winNum must be between 1 and the board size")

        temp_grid = []

        for row in range(board_size):
            temp_row = []
            for column in range(board_size):
                spot = self.grid[row][column]
                character = spot.get_state()

                if character == '?' and spot.is_entangled():
                    self._measure_pair(spot, pool)
                    character = spot.get_state()
                elif character == '?' and spot.is_wave():
                    self._make_definite(spot, 'X' if pool.randbelow(2) == 0 else 'O')
                    character = spot.get_state()
                elif character == '?':
                    tilt_a = spot.get_tiltA()
                    tilt_b = spot.get_tiltB()
                    total = tilt_a + tilt_b

                    if total <= 0:
                        raise ValueError("The sum of tiltA and tiltB must be positive")

                    probability = tilt_a / total
                    character = 'X' if pool.random() < probability else 'O'
                    spot.set_state(character)

                temp_row.append(character)
            temp_grid.append(temp_row)

        directions = (
            (0, 1),
            (1, 0),
            (1, 1),
            (1, -1),
        )

        for row in range(board_size):
            for column in range(board_size):
                character = temp_grid[row][column]
                if character not in ('X', 'O'):
                    continue

                for row_step, column_step in directions:
                    end_row = row + (winNum - 1) * row_step
                    end_column = column + (winNum - 1) * column_step

                    if not (0 <= end_row < board_size and 0 <= end_column < board_size):
                        continue

                    if all(
                        temp_grid[row + step * row_step][column + step * column_step] == character
                        for step in range(winNum)
                    ):
                        return character

        return None