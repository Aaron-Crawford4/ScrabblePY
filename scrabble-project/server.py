import socket                                         
import time
import json
from round import Round
import pygame
from sys import exit
from board import Board
from player import Player
from wordbank import collection_of_letters
from location import letter_locator
from button import button_locator
from round import Round
from word import Word
from _thread import *

# create a socket object
host = socket.gethostname()
port = 9999 # Socket on host 9999
ThreadCount = 0 # Number of threads the server is running
userList = {}
round = Round()
board = Board()
board.start_board()
words_placed = [] # Collection of all the letters placed
word = Word()
letter_storage = collection_of_letters() # Collection of all the letters that can be given

def clientHandler(connection, name):
    global total, userList, board, letter_storage, word, words_placed # Create global objects so that the threads can access them
    while True:
        data = connection.recv(2048) # Receive message
        message = data.decode('utf-8')
        if message == 'Not go': # If it isnt the clients go send them an update of the board
            dataBeingSent = { 'map': board.display_board, 'round': round.round, 'player' : {'name': userList[name].name, 'score': userList[name].score.score, 'turn':userList[name].turn,'inventory': {}}}
            total = 0
            for item in userList[name].inventory:
                dataBeingSent['player']['inventory'][total] = item.letter
                total += 1
            dataBeingSent = json.dumps(dataBeingSent).encode('utf-8')
            connection.sendall(dataBeingSent) # Send the information over so the client can update their board
        else:
            seperate = message.split('-') # If it is the clients go
            first_position = (int(seperate[0]), int(seperate[1]))
            second_position = (int(seperate[2]), int(seperate[3]))
            letter_locator(board, userList[name], first_position, second_position, word) # Update the board as to what letter they have placed
            words_placed, userList = button_locator(board, userList[name], userList, first_position, second_position, round, letter_storage, word, words_placed) # Check did they click either of the 3 buttons
            dataBeingSent = { 'map': board.display_board, 'round': round.round, 'player' : {'name': userList[name].name, 'score': userList[name].score.score, 'turn':userList[name].turn,'inventory': {}}}
            total = 0
            for item in userList[name].inventory:
                dataBeingSent['player']['inventory'][total] = item.letter
                total += 1
            dataBeingSent = json.dumps(dataBeingSent).encode('utf-8')
            connection.sendall(dataBeingSent) # Send over the updated data to the client

# Accepting new clients
def acceptConnections(serverSocket):

    Client, addr = serverSocket.accept()
    if len(userList) == 0: # If it is the first user then they are Player 1 and it is their go
        userList[addr[1]] = Player('Player 1', True)
        userList[addr[1]].fill_inventory(letter_storage) # Fill their inventory with letters
    else: # If it is not the first user work out which user it is
        name = 'Player ' + str(len(userList) + 1) # Assign them their name
        userList[addr[1]] = Player(name)
        userList[addr[1]].fill_inventory(letter_storage) # Fill their inventory with letters
    start_new_thread(clientHandler, (Client, addr[1])) # Create a new thread of the clienthandler with the information

# Starting the server
def startServer(host, port):
    serverSocket = socket.socket()
    try:
        serverSocket.bind((host, port)) # Give it the host and port
    except socket.error as e:
        print(e)
    print(f'Server listening on port {port}.')
    serverSocket.listen()

    while True: # Loop through accepting new clients when they request to join
        acceptConnections(serverSocket)

startServer(host, port) # Start the server