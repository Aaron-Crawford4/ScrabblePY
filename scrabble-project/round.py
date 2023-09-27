# Round class 
class Round:

    def __init__(self, round=1): # Start the round class
        self.round = round

    def increase(self): # Increase the round
        self.round += 1