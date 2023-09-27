from word import Word
import copy
from tile import Tile

# Location of score bonus
triple = [(0,0),(14,0),(0,14),(14,14),(7,14),(14,7),(0,7),(7,0)]
double = [(1,1),(2,2),(3,3),(4,4),(1,13),(2,12),(3,11),(4,10),(13,1),(12,2),(11,3),(10,4),(13,13),(12,12),(11,11),(10,10)]
triple_letter = [(1,5),(1,9),(5,1),(5,5),(5,9),(5,13),(9,1),(9,5),(9,9),(9,13),(13,5),(13,9)]
double_letter = [(0,3),(0,11),(2,6),(3,7),(2,6),(3,0),(3,14),(6,2),(6,6),(6,8),(6,12),(7,3),(8,2),(8,6),(8,8),(8,12),(11,0),(11,7),(11,14),(12,6),(12,8),(14,3),(14,11),(9,5),(2,8),(7,11)]

def locate_word(word, board, words_placed, player): # Get the location fo the word
    full_word = word.word_as_str() # Sorts the word to be in the correct order
    word.save_edge_cases() # Saves the start and end of the word
    if collateral_words(word, board, words_placed, player) != True: # Checks to see if in contact with any other word
        word.clear_list()
        return
    if check_dictionary(word, words_placed, player) == True: # Checks to make sure word is a valid dictionary word
        return
    word.clear_list()

def check_dictionary(word, words_placed,player):

    full_word = word.word_as_str() # Get the word as a string and not tile list
    with open("acceptable_words.txt", "r") as f: # Open the acceptable words file and read through it line by line
        for line in f:
            dictionary_word = line.rstrip()
            if dictionary_word == full_word: # If the word is in the file it is valid
                player.score.add_to_score(word, triple, double, triple_letter, double_letter) # Add to score
                words_placed.append(Word(copy.deepcopy(word.word_list), copy.deepcopy(word.direction), copy.deepcopy(word.edge_cases))) # Append the word to valid words placed
                return True
    return False

# Collateral_words
def collateral_words(word, board, words_placed,player):
    direction = word.direction
    in_front(word, board, words_placed, direction) # Check in front of the word
    behind(word, board, words_placed, direction) # Check behind the word
    if direction == "h":
        distance_from_start_to_end = word.edge_cases[1][0] - word.edge_cases[0][0] + 1 # distance from first letter to last letter
        horizontal = word.edge_cases[0][1]
        vertical = word.edge_cases[0][0]
        i = 0
        current_letter = 0
        while i < distance_from_start_to_end: # Loop through the word checking for its letters
            if (vertical, horizontal) == word.word_list[current_letter].board_location: # If coordinate in the word list then check the letter
                if vertical >= word.original_edge_cases[0][0] and word.original_edge_cases[1][0] >= vertical:
                    if side_check(word.word_list[current_letter],(vertical, horizontal), direction, board, words_placed,player,word) != True: # Check to make sure the letter is not ruining other words
                        return False
            else: # If a location has no letter placed by the user then it means their is a letter already placed that has to be added
                word.contact = True
                word.add_to_list(board.board[horizontal][vertical]), word.sort_list() # Add that letter to the word list
            current_letter += 1
            vertical += 1
            i += 1

    if direction == "v":
        distance_from_start_to_end = word.edge_cases[1][1] - word.edge_cases[0][1] + 1
        horizontal = word.edge_cases[0][1]
        vertical = word.edge_cases[0][0]
        i = 0
        current_letter = 0
        while i < distance_from_start_to_end: # Loop through the word checking for its letters
            if (vertical, horizontal) == word.word_list[current_letter].board_location: # If coordinate in the word list then check the letter
                if horizontal >= word.original_edge_cases[0][1] and word.original_edge_cases[1][1] >= horizontal:
                    if side_check(word.word_list[current_letter],(vertical, horizontal), direction, board, words_placed,player,word) != True: # Check to make sure the letter is not ruining other words
                        return False
            else: # If a location has no letter placed by the user then it means their is a letter already placed that has to be added
                word.contact = True
                word.add_to_list(board.board[horizontal][vertical]), word.sort_list() # Add that letter to the word list
            current_letter += 1
            horizontal += 1
            i += 1
    return True

# Side check, is used for checking either side of a letter to make sure that it is not in the way of another word already placed
def side_check(tile, location, direction, board, words_placed,player,word):
    if direction == "h": # Checks direction of tile
        if board.board[location[1]- 1][location[0]].letter != ' ': # If the tile beside the letter is not empty then check what word is placed
            word.made_contact() # Our word is making contact with another word
            tmp = False
            for word in words_placed:
                if word.direction != direction:
                    for point in word.edge_cases: # Check if we are on an edge case of a word which would mean we would have to extend that word
                        if point == (location[0], location[1] - 1): # If it is an edge case of a word
                            word.add_to_list(tile) # Add our tile to that word and check if it is valid
                            word.sort_list()
                            if check_dictionary(word, words_placed,player) != True: # If the word is valid then continue
                                return False # If not valid then return with a false
                            tmp = True # Set tmp to true as we have checked the side
                            break
            if tmp != True: # If tmp is not true then we have to check what word we are in contact with as we failed to find an edge case
                for word in words_placed:
                    if word.direction == direction: # Our word directions would be similar as it is not an edge case we are in contact with
                        for object in word.word_list:
                            if object.board_location == (location[0], location[1] - 1): # If we found the coordinate of a word
                                new_word = Word([tile, object], direction, ((object.board_location),(location[0], location[1] - 1))) # create a new word with the new tile location
                                new_word.save_edge_cases() # Save the edge cases of that word
                                if check_dictionary(new_word, words_placed,player) != True: # If the word is valid then continue
                                    return False # If not valid then return with a false
        # Similar method as above but just checking the opposite side of the word
        if board.board[location[1]+ 1][location[0]].letter != ' ':
            word.made_contact()
            tmp = False
            for word in words_placed:
                if word.direction != direction:
                    for point in word.edge_cases:
                        if point == (location[0], location[1] + 1):
                            word.add_to_list(tile)
                            word.sort_list()
                            if check_dictionary(word, words_placed,player) != True:
                                return False
                            tmp = True
                            break
            if tmp != True:
                for word in words_placed:
                    if word.direction == direction:
                        for object in word.word_list:
                            if object.board_location == (location[0], location[1] + 1):
                                new_word = Word([tile, object], direction, ((object.board_location),(location[0], location[1] + 1)))
                                new_word.save_edge_cases()
                                if check_dictionary(new_word, words_placed,player) != True:
                                    return False
    if direction == "v": # When a word is vertical it is the same method as horizontal but instead of changing the y coordinate, we change the x coordinate for this one as it is vertical not horizontal
        if board.board[location[1]][location[0] - 1].letter != ' ': # Same code applies as the above method
            word.made_contact()
            tmp = False
            for word in words_placed:
                if word.direction != direction:
                    for point in word.edge_cases:
                        if point == (location[0] - 1, location[1]):
                            word.add_to_list(tile)
                            word.sort_list()
                            if check_dictionary(word, words_placed,player) != True:
                                return False
                            tmp = True
                            break
            if tmp != True:
                for word in words_placed:
                    if word.direction == direction:
                        for object in word.word_list:
                            if object.board_location == (location[0] - 1, location[1]):
                                new_word = Word([tile, object], direction, ((object.board_location),(location[0] - 1, location[1])))
                                new_word.save_edge_cases()
                                if check_dictionary(new_word, words_placed,player) != True:
                                    return False
        if board.board[location[1]][location[0] + 1].letter != ' ':
            word.made_contact()
            tmp = False
            for word in words_placed:
                if word.direction != direction:
                    for point in word.edge_cases:
                        if point == (location[0] + 1, location[1]):
                            word.add_to_list(tile)
                            word.sort_list()
                            if check_dictionary(word, words_placed,player) != True:
                                return False
                            tmp = True
                            break
            if tmp != True:
                for word in words_placed:
                    if word.direction == direction:
                        for object in word.word_list:
                            if object.board_location == (location[0]+ 1, location[1]):
                                new_word = Word([tile, object], direction, ((object.board_location),(location[0]+ 1, location[1])), True)
                                new_word.save_edge_cases()
                                if check_dictionary(new_word, words_placed,player) != True:
                                    return False
    return True # Return true if all checks passed succesfully


# Checks in front of the first letter to see if we are extending an already made word
def in_front(word, board, words_placed, direction):
    if direction == "h": # If its horizontal change the coordinate to 1 in front
        front_check = (word.edge_cases[0][0] - 1, word.edge_cases[0][1])
    else: # If its vertical change the coordinate to 1 in front
        front_check = (word.edge_cases[0][0], word.edge_cases[0][1] - 1)
    if board.board[front_check[1]][front_check[0]].letter != ' ': # If there is a letter combine it to the word
        word.made_contact()
        word_combiner(board.board[front_check[1]][front_check[0]], word, board, words_placed, direction)

# Checks behind of the last letter to see if we are extending an already made word
def behind(word, board, words_placed, direction):
    if direction == "h": # If its horizontal change the coordinate to 1 inbehind
        back_check = (word.edge_cases[1][0] + 1, word.edge_cases[1][1])
    else: # If its vertical change the coordinate to 1 in front
        back_check = (word.edge_cases[1][0], word.edge_cases[1][1] + 1)
    if board.board[back_check[1]][back_check[0]].letter != ' ': # If there is a letter combine it to the word
        word.made_contact()
        word_combiner(board.board[back_check[1]][back_check[0]], word, board, words_placed, direction)

# word combiner will combine tiles of other words to the word we are checking if they are in contact
def word_combiner(tile, word, board, words_placed, direction):
    tmp_storage = []
    for item in words_placed:
        if item.direction == direction: # If the words are in the same direction
            for object in item.word_list:
                if tile.location == object.location: # If we found the tile that needs to be added combine the words
                    tmp_storage.append(item.edge_cases)
                    words_placed.remove(item)
                    word.combine_words(item) # Combine the words
                    word.word_as_str()
                    return
    for item in words_placed:
        if item.direction != direction: # If the words are in opposite directions
            for object in item.word_list:
                if tile.location == object.location: # If we found the tile that needs to be added
                    tmp_storage.append(item.edge_cases)
                    word.add_to_list(Tile(tile.letter, tile.location, tile.board_location)) # Add the singular tile as they are in opposite directions
                    word.word_as_str()