

class QQQBlock:
    def __init__(self, state = '-'):
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
        return self.partner is not None

    def is_wave(self):
        return self.wave_origin is not None

    def direct_add(self, value):
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
        return self.state

    def set_state(self, state):
        self.state = state
        
    def get_tiltA(self):
        return self.tiltA

    def set_tiltA(self, tilt):
        self.tiltA = tilt
    
    def get_tiltB(self):
            return self.tiltB
    
    def set_tiltB(self, tilt):
        self.tiltB = tilt