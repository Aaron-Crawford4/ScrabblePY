from score import Score
from tile import Tile
import random
import copy
from wordbank import collection_of_letters

# Player class
class Player:

    def __init__(self, name, turn=False):
        self.name = name 
        self.score = Score() 
        self.turn = turn 
        self.display_inventory = []
        self.database_display_inventory = []
        self.inventory = []
        self.database_inventory = []

    def switch_turn(self): # Switch the turn of the player from turn to false, or false to true
        if self.turn == True:
            self.turn = False
            return
        else:
            self.turn = True

    def fill_inventory(self, list):
        amount = self.total_inventory() # Gets the amount of letters in inventory
        for x in range(7 - amount): # if less then 7 fills them back up
            place = random.randint(0, (len(list) - 1)) # takes from the letter storage
            letter = list[place]
            list.pop(place)
            self.inventory.append(Tile(letter))
            self.display_inventory.append(letter)
        self.save_inventory() # Saves the inventory

    def refresh_inventory(self, list): # Refresh inventory
        tmp = self.inventory # Saves a tmp inventory to hold the existing letters
        self.inventory.clear() # Empty the inventory
        for x in range(7): # Refill the inventory
            place = random.randint(0, (len(list) - 1))
            letter = list[place]
            list.pop(place)
            self.inventory.append(Tile(letter))
            self.display_inventory.append(letter)
        self.save_inventory() #Save changes
        for item in tmp: # Add in the original letters back to the inventory
            list.append(item.letter)

    def save_inventory(self): # Save inventory, saves both inventorys to the database_inventory
        self.database_inventory = copy.deepcopy(self.inventory)
        self.database_display_inventory = copy.deepcopy(self.display_inventory)

    def reload_inventory(self): # reload inventory, saves the database_inventory to the normal inventory
        self.inventory = copy.deepcopy(self.database_inventory)
        self.display_inventory = copy.deepcopy(self.database_display_inventory)

    def total_inventory(self): # Total inventory gets the amount of letters in the inventory
        return len(self.inventory)

    def display_name(self): # Returns the clients name
        return self.name 