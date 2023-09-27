from email import message
import socket
import pygame
from board import Board
from player import Player
from round import Round
import json

host = socket.gethostname()                           
port = 9999 # Use port 9999


# Update game refreshes the UI when information is received from the server
def update_game(data, board, player, round):
    player.name = data['player']['name']
    player.score = data['player']['score']
    player.turn = data['player']['turn']
    player.display_inventory.clear()
    for key, item in data['player']['inventory'].items():
        player.display_inventory.append(item)
    board.display_board = data['map']
    round.round = data['round']
    pass

# Attempts to connect with the server
def connect_to_server():
    ClientSocket = socket.socket()
    print('Waiting for connection')
    try:
        ClientSocket.connect((host, port))
        print("works")
    except socket.error as e:
        print(str(e))
    connected_int = 1
    return ClientSocket, connected_int

# Sends the infromation to the server everytime a click happens
def connected(ClientSocket, first_position, second_position):
    messageToSend = f'{str(first_position[0])}-{str(first_position[1])}-{str(second_position[0])}-{str(second_position[1])}'
    ClientSocket.send(str.encode(messageToSend))
    response = ClientSocket.recv(2048)
    return json.loads(response.decode('utf-8'))

# Loops requests to the server to keep updated with what other users are doing on the board
def loop_request(ClientSocket):
    messageToSend = f'Not go'
    ClientSocket.send(str.encode(messageToSend))
    response = ClientSocket.recv(2048)
    
    return json.loads(response.decode('utf-8'))

# Help command screen which shows the help screen
def help_command(screen):
    font = pygame.font.SysFont(None, 80) # Sets font for letters
    screen.fill('black')
    text = font.render("Bonus Points", True, 'white') 
    screen.blit(text, (235, 20))
    font = pygame.font.SysFont(None, 40) # Sets font for letters
    pygame.draw.rect(screen, '#FF0000', (100,340, 60,60))
    text = font.render("Triple Word", True, 'white') 
    screen.blit(text, (170, 360))
    pygame.draw.rect(screen, '#F0FF3F', (100,260, 60,60))
    text = font.render("Double Word", True, 'white') 
    screen.blit(text, (170, 280))
    pygame.draw.rect(screen, '#59F5FF', (100,100, 60,60))
    text = font.render("Double Letter", True, 'white') 
    screen.blit(text, (170, 120))
    pygame.draw.rect(screen, '#3C8AFF', (100,180, 60,60))
    text = font.render("Triple letter", True, 'white') 
    screen.blit(text, (170, 200))
    pygame.draw.rect(screen, '#3C8AFF', (100,180, 60,60))
    text = font.render("Triple letter", True, 'white') 
    screen.blit(text, (170, 200))

    pygame.draw.rect(screen, 'red', (350,900, 150,50))
    text = font.render("Back", True, 'white') 
    screen.blit(text, (390, 915))
    return 2

# Checks if join game or how to play were clicked
def button_check(first_postion, screen):
    x = first_postion[0]
    y = first_postion[1]
    if x >= 325 and x <= 525 and y >= 420 and y <= 480:
        return connect_to_server()

    if x >= 325 and x <= 525 and y >= 510 and y <= 570:
        return None, help_command(screen)
    return None, 0

# When on help screen checks if the back button was clicked
def button_back_check(first_postion, screen):
    x = first_postion[0]
    y = first_postion[1]
    if x >= 350 and x <= 500 and y >= 900 and y <= 950:
        display_main_screen(screen)
        return 0
    return 2

# Displaus the main UI screen with the 2 options on what to do
def display_main_screen(screen):
    screen.fill('black')
    font = pygame.font.SysFont(None, 50) # Sets font for letters
    text = font.render("Join Game", True, 'white') 
    pygame.draw.rect(screen, '#1982FC', (325, 420, 200,60))
    screen.blit(text, (335, 435))

    font = pygame.font.SysFont(None, 50) # Sets font for letters
    text = font.render("How to Play", True, 'white')
    pygame.draw.rect(screen, '#027900', (325, 510, 200,60))
    screen.blit(text, (328, 525))

def main():

    pygame.init()
    screen = pygame.display.set_mode((850,1000))
    pygame.display.set_caption('Scrabble')
    clock = pygame.time.Clock()
    board = Board()
    round = Round()
    player = Player('tmp')
    display_main_screen(screen)
    connected_int = 0 # Used to distinguish what screen we are on, 0 being home screen, 1 being game screen, 2 being help screen
    while True:
        clock.tick(10)
        if connected_int == 1: # If on game screen update the board with the information
            board.draw_board(screen, round)
        if player.name != 'tmp':
            board.draw_inventory(screen, player)
        for event in pygame.event.get(): # Event check
            if event.type == pygame.QUIT: # Quit is clicked exit the game
                if connected_int == 1:
                    ClientSocket.close()
                pygame.quit() # Closes the window
                exit() # Exits without an error
            elif event.type == pygame.MOUSEBUTTONDOWN: # On mousebutton down check what was clicked
                first_position = event.pos
                if connected_int == 0: # If on home screen check which button was clicked
                    ClientSocket, connected_int = button_check(first_position, screen)
                if connected_int == 2: # If on help screen check if back was clicked
                    connected_int = button_back_check(first_position, screen)
            elif event.type == pygame.MOUSEBUTTONUP: # On mousebutton up check where was clicked
                if player.turn == True:
                    second_position = event.pos
                    if connected_int == 1: # If on game screen send the information to the server
                        data = connected(ClientSocket, first_position, second_position)
                        update_game(data, board, player, round) # Use the information to update the game
        if connected_int == 1: # If on game screen continue with the loop rquest
            data = loop_request(ClientSocket)
            update_game(data, board, player, round) 

        pygame.display.update() # Update the pygame display      

main()