
class QQQBlock:
    def __init__(self, state = '-', super:bool = False):
        self.state = state
        self.tiltA = 0
        self.tiltB = 0
        self.super = super

    def direct_add(self, value):
        self.state = value
        self.super = False

    def get_state(self):
        return self.state

    def set_state(self, state):
        self.state = state