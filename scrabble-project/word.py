from tile import Tile
import copy

class Word:

    def __init__(self, word_list=[], direction="", edge_cases=(), original_edge_cases=(), contact=False, dont_switch=False):
        self.word_list = word_list
        self.direction = direction
        self.edge_cases = edge_cases
        self.original_edge_cases = original_edge_cases
        self.contact = contact
        self.dont_switch = dont_switch

    def change_direction(self): # Change direction of word, used for single words being added to an already placed word
        if self.direction == "v":
            self.direction = "h"
        else:
            self.direction = "v"

    def made_contact(self): # Make contact set to True
        self.contact = True

    def check_contact(self): # Check if contac is made
        return self.contact

    def add_to_list(self, tile): # Add tile to list
        self.word_list.append(tile)

    def clear_list(self): # Empty list
        self.word_list.clear()
        self.contact = False

    def is_empty(self): # Check if list is empty
        return len(self.word_list)

    def word_as_str(self): # Conver word list to string
        self.duplicate_check() # Check to make sure no duplicates
        self.sort_list() # Sort list so its in the correct order
        straight = "" # Set a string
        for tile in self.word_list: # Loop through the list
            straight += tile.letter 
        return straight # Return string

    def save_edge_cases(self): # Save edge cases
        self.original_edge_cases = self.edge_cases

    def sort_list(self): # Sorts list on whichever coordinate is not the same
        co_ordinate = self.co_ordinate_find() # Find which coordinate is similar between all elements
        if co_ordinate == -1: # -1 means a error was made and the word is invalid
            return self.clear_list()
        self.word_list.sort(key=lambda x : x.location[co_ordinate])
        self.edge_cases = ((((self.word_list[0].location[0] - 60) // 50), ((self.word_list[0].location[1] - 60) // 50)), (((self.word_list[-1].location[0] - 60) // 50), ((self.word_list[-1].location[1] - 60) // 50)))

    def combine_words(self, new): # Combine 2 words together to make 1 word
        self.word_list = self.word_list + new.word_list
        self.sort_list()

    def co_ordinate_find(self): # Find which coordinate is similar between the list
        if self.dont_switch == True: # Used for single words to prevent them switching the direction
            if self.direction == "v":
                return 1
            else:
                return 0

        base = self.word_list[0].location[0], self.word_list[0].location[1] # first location
        similar_x = True
        similar_y = True
        for tile in self.word_list: # Loop through and see which coordinate statys the same
            if tile.location[0] != base[0] and similar_x == True:
                similar_x = False
            if tile.location[1] != base[1] and similar_y == True:
                similar_y= False
        if similar_x == True: # Return whichever is true as that is the coordinate that is the same
            self.direction = "v"
            return 1
        elif similar_y == True:
            self.direction = "h"
            return 0
        else:
            return -1

    def duplicate_check(self): # Checks for duplicates in the word list, and removes them
        tmp = []
        i = 0
        while (i < len(self.word_list)):
            tile = self.word_list[i]
            if tile.board_location not in tmp:
                tmp.append(tile.board_location)
                i += 1
            else:
                self.word_list.remove(tile)