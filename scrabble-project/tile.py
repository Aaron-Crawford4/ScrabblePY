

class Tile:

    def __init__(self, letter, location=(0,0), board_location=(0,0)):
        self.letter = letter
        self.location = location
        self.board_location = board_location

    def show_location(self): # Gets the location of a tile
        return self.location

    def change_location(self, new_location, new_board_location=(0,0)): # Switches location of tile
        self.location = new_location
        self.board_location = new_board_location

    def change_letter(self, new_letter): # Changes tile letter
        self.letter = new_letter