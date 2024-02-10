class Player:
    def __init__(self, name, risk_factor):
        self.name = name
        self.risk_factor = risk_factor
        self.win = 0

    def get_name(self):
        return self.name

    def get_risk_factor(self):
        return self.risk_factor

    def get_win(self):
        return self.win

    def set_win(self, win):
        self.win = win

