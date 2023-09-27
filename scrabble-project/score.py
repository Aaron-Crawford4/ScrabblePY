
class Score:

    def __init__(self):
        self.score = 0 # Keeps score
        self.backup_score = 0

    def save_to_score(self): # Save the score
        self.score = self.backup_score

    def reset_score(self): # Reset the score, because word was rejected
        self.backup_score = self.score

    def add_to_score(self, word, triple, double, triple_letter, double_letter): # Add to score
        multiplier = self.check_word_bonus(word, triple, double) # Check if letters on a bonus word tile
        for tile in word.word_list:
            self.backup_score += (self.check_amount(tile.letter) * self.check_letter_bonus(tile, triple_letter, double_letter)) * multiplier # Check if letters on a bonus letter tile and multiply by bonus word if any

    def check_amount(self, letter): # Check value of letter
        if letter == 'a' or letter == 'e' or letter == 'i' or letter == 'l' or letter == 'n' or letter == 'o' or letter == 'r' or letter == 's' or letter == 't' or letter == 'u':
            return 1
        elif letter == 'd'  or letter == 'g':
            return 2
        elif letter == 'b' or letter == 'c' or letter == 'm' or letter == 'p':
            return 3
        elif letter == 'f' or letter == 'h' or letter == 'v' or letter == 'w' or letter == 'y':
            return 4
        elif letter == 'k':
            return 5
        elif letter == 'j' or letter == 'x':
            return 8
        elif letter == 'q' or letter == 'z':
            return 10
        else:
            return 0

    def check_letter_bonus(self, letter, triple_letter, double_letter): # Check to see if letter gets a bonus
        points = 1
        if letter.board_location in triple_letter: # If their is a bonus add it to the points 
            points = points * 3
            triple_letter.remove(letter.board_location) # Remove bonus location so cant be reused
        elif letter.board_location in double_letter:
            points = points * 2
            double_letter.remove(letter.board_location)
        return points

    def check_word_bonus(self, word, triple, double): # Check to see if word gets a bonus
        points = 1
        for tile in word.word_list: # loop through word
            if tile.board_location in triple:  # If their is a bonus add it to the points 
                points = points * 3
                triple.remove(tile.board_location) # Remove bonus location so cant be reused
            elif tile.board_location in double:
                points = points * 2
                double.remove(tile.board_location)
        return points