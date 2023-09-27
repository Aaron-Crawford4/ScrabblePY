from word_finder import locate_word
import copy

# Button locator is used to check if the client clicked either of the 3 buttons
def button_locator(board, player, players, first_click, second_click, round, letter_storage, word, words_placed): # Switches which player is currently playing

    x = first_click[0]
    y = first_click[1]
    if x >= 480 and x <= 600 and y >= 900 and y <= 940: # Checks the location where the client could be clicking
        words_placed, players = submit_button(board, player, players, round, letter_storage, word, words_placed) # If the submit button was clicked then pass to function

    if x >= 620 and x <= 740 and y >= 900 and y <= 940: # Checks the location where the client could be clicking
        reset_button(board, player, word) # If the reset button was clicked then pass to function

    if x >= 510 and x <= 710 and y >= 950 and y <= 990: # Checks the location where the client could be clicking
        players = refresh_hand(board, player, players, letter_storage,word) # If the refresh button was clicked then pass to function

    return words_placed, players

def submit_button(board, player, players, round, letter_storage, word, words_placed):
    if word.is_empty() == 0: # Checks to make sure letters have been placed
        return words_placed, players
    # Makes a backup of the total words placed and a backup of the word
    words_placed_backup = copy.deepcopy(words_placed) # Incase the inputted word doesnt fit a backup of all placed words is made
    backup = copy.deepcopy(word)
    # Locate the word on the board and error check its positioning and contact with other words
    locate_word(word, board, words_placed_backup, player)
    if len(backup.word_as_str()) == 1 and word.check_contact() == False: # If the word has 1 letter check both the horizontal and vertical axis
        player.score.reset_score() # Rest the information that the previous check went through
        words_placed_backup = copy.deepcopy(words_placed) # Reset the copys
        word = copy.deepcopy(backup) # Reset the copys
        word.change_direction() # Switch the direction of the word to check the opposite axis
        word.dont_switch = True # Set dont_Switch to True to not switch the axis again
        locate_word(word, board, words_placed_backup, player)
    
    if word.is_empty() == 0: # If an empty word is returned then it was not valid
        reset_button(board, player, word) # Reset the information
        player.score.reset_score() # Reset the score
        return words_placed, players
    
    if word.check_contact() == False: # If the word is not in contact with an already placed letter then
        if round.round != 1:
            reset_button(board, player, word)
            player.score.reset_score()
            return words_placed, players
        else: # Check it goes through the middle of the board which would indicate it is valid
            tmp_value = False
            for item in word.word_list:
                if item.board_location == (7,7):
                    tmp_value = True
                    break
            if tmp_value == False:
                reset_button(board, player, word)
                player.score.reset_score()
                return words_placed, players
    
    words_placed = copy.deepcopy(words_placed_backup) # The word is then added to the overall collection of valid words placed
    
    i = 0 # Run through and switch the players turns
    for key in players:
        if players[key].turn == True:
            players[key].switch_turn()
            i += 1
            break
        i += 1
    k = 0
    if i == len(players):
        for key in players:
            if k == 0:
                players[key].switch_turn()
                break
    else:
        for key in players:
            if k == i:
                players[key].switch_turn()
                break
            k += 1
        
    round.increase() # Increase the round
    player.fill_inventory(letter_storage) # Refill the inventory
    player.score.save_to_score() # Add to their score
    word.clear_list() # Reset the tmp word holder
    board.save_board() # Save the changes to the board
    return words_placed, players

# Rest button, resets everything the user could have changed when placing letters
def reset_button(board, player, word):
    board.reload_board()
    player.reload_inventory()
    word.clear_list()

# Refresh hand replaces the uses inventory and moves the turn on
def refresh_hand(board, player, players, letter_storage, word):
    board.reload_board()
    word.clear_list()
    player.refresh_inventory(letter_storage) # Give them a new inventory

    # Switch the players turns
    i = 0
    for key in players:
        if players[key].turn == True:
            players[key].switch_turn()
            i += 1
            break
        i += 1
    k = 0
    if i == len(players):
        for key in players:
            if k == 0:
                players[key].switch_turn()
                break
    else:
        for key in players:
            if k == i:
                players[key].switch_turn()
                break
            k += 1
    return players
