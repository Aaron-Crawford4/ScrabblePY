import pygame
import sys
from tile import Tile
import copy

class Board:
    def __init__(self):
        self.board = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]] # Will be used for the storage
        self.database_board = []
        self.display_board =   [[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                                [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                                [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                                [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                                [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                                [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                                [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                                [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                                [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                                [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                                [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                                [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                                [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                                [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                                [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],]
        self.database_display_board = []
    
    def start_board(self):
        for y in range(0,15): # Loops through and makes each box
            for x in range(0,15):
                if self.board[y][x] == 0: # Replace 0 with tile object
                    self.board[y][x] = Tile( ' ',((60 + (x * 50)), (60 + (y * 50))), (x,y))
                    if x == 14 and y == 14: # On the last piece copy the board to the main board
                        self.save_board() 

    def start_inventory(self, player):
        for tile in player.inventory: # Displays each letter
            tile.change_location(((60 + (i)),900))
            i += 50

    def draw_board(self, win, round):
        win.fill("black")
        pygame.draw.rect(win, 'indianred', (30,30,800,800)) # Displays border
        pygame.draw.rect(win, 'white', (50,50,760,760)) # Displays seperators between boxes
        for y in range(0,15): # Loops through and makes each box
            for x in range(0,15):
                if self.board[y][x] == 0: # Replace 0 with tile object
                    self.board[y][x] = Tile( ' ',((60 + (x * 50)), (60 + (y * 50))), (x,y))
                    self.display_board[y][x] = ' '
                    if x == 14 and y == 14: # On the last piece copy the board to the main board
                        self.save_board() 

                if (x == 0 and y == 0) or (x == 14 and y == 0) or (x == 0 and y == 14) or (x == 14 and y == 14) or (x == 7 and y == 14) or (x == 14 and y == 7) or (x == 0 and y == 7) or (x == 7 and y == 0):
                    pygame.draw.rect(win, '#FF0000', ((60 + (x * 50)),(60 + (y * 50)), 40,40))
                    font = pygame.font.SysFont(None, 40) # Sets font for letters
                    text = font.render(self.display_board[y][x], True, (255, 0, 0))
                    win.blit(text, (70 + (x * 50), (67 + (y * 50))))
                elif (x == 1 and y == 1) or (x == 2 and y == 2) or (x == 3 and y == 3) or (x == 4 and y == 4) or (x == 1 and y == 13) or (x == 2 and y == 12) or (x == 3 and y == 11) or (x == 4 and y == 10) or (x == 13 and y == 1) or (x == 12 and y == 2) or (x == 11 and y == 3) or (x == 10 and y == 4) or (x == 13 and y == 13) or (x == 12 and y == 12) or (x == 11 and y == 11) or (x == 10 and y == 10):
                    pygame.draw.rect(win, '#F0FF3F', ((60 + (x * 50)),(60 + (y * 50)), 40,40))
                    font = pygame.font.SysFont(None, 40) # Sets font for letters
                    text = font.render(self.display_board[y][x], True, (255, 0, 0))
                    win.blit(text, (70 + (x * 50), (67 + (y * 50))))
                elif (x == 0 and y == 3) or (x == 0 and y == 11) or (x == 2 and y == 6) or (x == 3 and y == 7) or (x == 2 and y == 6) or (x == 3 and y == 0) or (x == 3 and y == 14) or (x == 6 and y == 2) or (x == 6 and y == 6) or (x == 6 and y == 8) or (x == 6 and y == 12) or (x == 7 and y == 3) or (x == 8 and y == 2) or (x == 8 and y == 6) or (x == 8 and y == 8) or (x == 8 and y == 12) or (x == 11 and y == 0) or (x == 11 and y == 7) or (x == 11 and y == 14) or (x == 12 and y == 6) or (x == 12 and y == 8) or (x == 14 and y == 3) or (x == 14 and y == 11) or (x == 2 and y == 8) or (x == 7 and y == 11):
                    pygame.draw.rect(win, '#59F5FF', ((60 + (x * 50)),(60 + (y * 50)), 40,40))
                    font = pygame.font.SysFont(None, 40) # Sets font for letters
                    text = font.render(self.display_board[y][x], True, (255, 0, 0))
                    win.blit(text, (70 + (x * 50), (67 + (y * 50))))
                elif (x == 1 and y == 5) or (x == 1 and y == 9) or (x == 5 and y == 1) or (x == 5 and y == 5) or (x == 5 and y == 9) or (x == 5 and y == 13) or (x == 9 and y == 1) or (x == 9 and y == 5) or (x == 9 and y == 9) or (x == 9 and y == 13) or (x == 13 and y == 5) or (x == 13 and y == 9):
                    pygame.draw.rect(win, '#3C8AFF', ((60 + (x * 50)),(60 + (y * 50)), 40,40))
                    font = pygame.font.SysFont(None, 40) # Sets font for letters
                    text = font.render(self.display_board[y][x], True, (255, 0, 0))
                    win.blit(text, (70 + (x * 50), (67 + (y * 50))))
                elif (x == 7 and y == 7):
                    pygame.draw.rect(win, '#000000', ((60 + (x * 50)),(60 + (y * 50)), 40,40))
                    font = pygame.font.SysFont(None, 40) # Sets font for letters
                    text = font.render(self.display_board[y][x], True, (255, 0, 0))
                    win.blit(text, (70 + (x * 50), (67 + (y * 50))))

                else:
                    pygame.draw.rect(win, '#989898', ((60 + (x * 50)),(60 + (y * 50)), 40,40))
                    font = pygame.font.SysFont(None, 40) # Sets font for letters
                    text = font.render(self.display_board[y][x], True, (255, 0, 0))
                    win.blit(text, (70 + (x * 50), (67 + (y * 50))))

        # Submit button code
        text = font.render("Submit", True, 'white') # Code for submit box
        pygame.draw.rect(win, 'blue', (480, 900, 120,40))
        win.blit(text, (490, 910))
        text = font.render("Reload", True, 'white') # Code for reload box
        pygame.draw.rect(win, 'red', (620, 900, 120,40))
        win.blit(text, (630, 910))
        text = font.render("Refresh Deck", True, 'white') # Code for reload box
        pygame.draw.rect(win, 'green', (510, 950, 200,40))
        win.blit(text, (520, 960))
        text = font.render(f'Round {round.round}', True, 'white') # Code for round
        win.blit(text, (375, 850))

    def draw_inventory(self, win, player):
        font = pygame.font.SysFont(None, 50) # Sets font for player name
        name = font.render(player.name, False, (255, 0, 0))# Displays player name 
        win.blit(name, (50, 860))
        tmp = font.render("Score", False, (255, 0, 0))
        win.blit(tmp, (200, 860))
        score = font.render(str(player.score), False, (255, 0, 0))
        win.blit(score, (320, 860))
        font = pygame.font.SysFont(None, 40) # Sets font for letters
        i = 0
        if player.turn == True:
            text = font.render(f'Your Go', True, 'white') # Code for round
            win.blit(text, (550, 850))
        for tile in player.display_inventory: # Displays each letter
            text = font.render(tile, True, (255, 0, 0))
            pygame.draw.rect(win, 'darkgrey', ((60 + (i)),(900), 40,40))
            win.blit(text, (70 + (i), 910))
            i += 50


    def save_board(self): # Saves the user inputs to the main board
        self.database_board = copy.deepcopy(self.board)
        self.database_display_board = copy.deepcopy(self.display_board)

    def reload_board(self): # Resets the user inputs to the main board
        self.board = copy.deepcopy(self.database_board)
        self.display_board = copy.deepcopy(self.database_display_board)