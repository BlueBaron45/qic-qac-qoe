from numpy.f2py.auxfuncs import throw_error


class QQQBlock:
    def __init__(self, state = '-'):
        self.state = state
        self.tiltA = 0
        self.tiltB = 0

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