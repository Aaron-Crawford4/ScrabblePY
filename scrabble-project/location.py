from tile import Tile
import pygame

NoneType = type(None)

def hand_letter(player, first_click, letter_check=0): # Letter check is used to keep track of the letter that will be removed
    x = first_click[0]
    y = first_click[1]
    for tile in player.inventory: # Loops through each letter in hand to check which is clicked
        if x >= (60 + (50 * letter_check)) and x <= (100 + (50 * letter_check)):
            if y >= 900 and y <= 940:
                return tile, letter_check # Returns the tile of the letter
                break
        letter_check += 1
    return NoneType, letter_check # If it cant find a letter returns NoneType

def map_letter(board, second_click): # Map letter works out where the client clicked on the board
    x = second_click[0]
    y = second_click[1]
    i = 0
    j = 0
    if (x < 60 or x > 800) or (y < 60 or y > 800): # Makes sure 0 isnt returned
        return (NoneType, NoneType)
    while x >= 60 and x <= 800: # Loops through gets x location
        if x >= (60 + (50 * i)) and x <= (100 + (50 * i)):
            break
        if i > 14: # If the x location isnt one of the boxes exits function
            return (NoneType, NoneType)
        i += 1

    while y >= 60 and y <= 800: # Loops through gets y location
        if y >= (60 + (50 * j)) and y <= (100 + (50 * j)):
            break
        if j > 14: # If the y location isnt one of the boxes exits function
            return (NoneType, NoneType)
        j += 1

    if board.board[j][i].letter != ' ':
        return (NoneType, NoneType)
    return (i,j)

# Letter locator, locates which postion the client has clicked on the board and what letter it corresponds with
def letter_locator(board, player, first_click, second_click, word):
    picked_letter, letter_check = hand_letter(player, first_click) # Locates the letter from inventory
    picked_box = map_letter(board, second_click) # Locates the box on the board
    if picked_box == NoneType or picked_box[1] == NoneType or picked_box[0] == NoneType or picked_letter == NoneType:
        return # If it cant find where it clicked it returns
    player.inventory.pop(letter_check) # Pop the tile from the inventory that is being moved
    board.board[picked_box[1]][picked_box[0]] = Tile(picked_letter.letter, (board.board[picked_box[1]][picked_box[0]].location), (picked_box[0],picked_box[1])) # Add the letter to the board
    board.display_board[picked_box[1]][picked_box[0]] = picked_letter.letter
    word.add_to_list(Tile(picked_letter.letter, (board.board[picked_box[1]][picked_box[0]].location), (picked_box[0],picked_box[1]))) # Add the letter to the word being built list