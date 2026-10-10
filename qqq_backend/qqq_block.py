from numpy.f2py.auxfuncs import throw_error


class QQQBlock:
    def __init__(self, state = '-', super:bool = False):
        self.state = state
        self.tiltA = 0
        self.tiltB = 0
        self.super = super

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