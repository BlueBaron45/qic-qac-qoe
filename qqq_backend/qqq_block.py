class QQQBlock:
    """Represent one board cell and its quantum state.

    A cell may be empty, contain a definite X/O move, be uncertain in a
    superposition, be entangled with another cell, or represent a wave created by
    interference. The class stores the current state and a few quantum metadata
    fields that the grid logic uses to resolve gameplay outcomes.
    """

    def __init__(self, state='-'):
        """Create a single cell with a default empty state."""
        self.state = state
        self.tiltA = 0
        self.tiltB = 0
        # entanglement link (None when the cell is not entangled)
        self.partner = None    # (row, column) of the other cell
        self.relation = None   # 'same' or 'opposite'
        self.tag = None        # letter shown on the board, e.g. 'a'

        # wave (interference) state: None when the cell is not a wave
        self.wave_origin = None   # symbol the cell had before it was split
        self.wave_phase = 0       # hidden number of phase shifts added so far

    def is_entangled(self):
        """Return True when this cell is linked to another cell by entanglement."""
        return self.partner is not None

    def is_wave(self):
        """Return True when the cell represents a wave/phase interference state."""
        return self.wave_origin is not None

    def direct_add(self, value):
        """Place a definite X or O mark into this cell.

        This is the standard move path. The function updates the tilt values that
        represent the relative preference for X and O, and if both sides are non-
        zero the cell becomes uncertain ('?').
        """
        if value == 'X':
            self.tiltA += 1
        elif value == 'O':
            self.tiltB += 1
        else:
            raise ValueError("Illegal move")
        if self.tiltA == 0:
            self.super = False
            self.state = 'O'
        elif self.tiltB == 0:
            self.super = False
            self.state = 'X'
        else:
            self.super = True
            self.state = '?'

    def get_state(self):
        """Return the visible cell state, for example '-', 'X', 'O', or '?'."""
        return self.state

    def set_state(self, state):
        """Set the visible state of the cell."""
        self.state = state

    def get_tiltA(self):
        """Return the X-side tilt strength for this cell."""
        return self.tiltA

    def set_tiltA(self, tilt):
        """Set the X-side tilt value used for probability calculations."""
        self.tiltA = tilt

    def get_tiltB(self):
        """Return the O-side tilt strength for this cell."""
        return self.tiltB

    def set_tiltB(self, tilt):
        """Set the O-side tilt value used for probability calculations."""
        self.tiltB = tilt