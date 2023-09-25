'''
Khizar Qureshi & Ntense Obono
Professor Matt Lepenski
pente.py
Sep 18 2023
API for two-player game of Pente
CS 347 - Advance Software Design 
'''

import flask
import json 
import sys
import argparse

app = flask.Flask(__name__)
games = {}
current = 0

'''Returns a string representation of the current board'''
def get_board(board):
    formatted_board = ""
    for row in board:
        for spot in row:
            formatted_board += spot 
    return formatted_board    

'''Determines if the player can be capturable'''
def is_capturable(board, row, col, char): 
    if col < 19 and board[row][col+1] == char and board[row][col]==char:
        return True
    elif row < 19 and board[row+1][col] == char and board[row][col]==char:
        return True
    elif row < 19 and col < 19 and board[row+1][col+1] == char and board[row][col]==char:
        return True
    elif col > 0 and board[row][col-1] == char and board[row][col]==char:
        return True
    elif row > 0 and board[row-1][col] == char and board[row][col]==char:
        return True
    elif row >0 and col > 0 and board[row-1][col-1] == char and board[row][col]==char:
        return True
    return False

'''Updates the amount of captures player X has from player O'''
def updateX(board,row,col):
    nums = 0
    if is_capturable(board,row,col,'o'): 
        if col < 18 and col > 1 and board[row][col+2] == "x" and board[row][col-2] == "x":
            nums+=1
        elif row < 18 and row > 1 and board[row+2][col] == "x" and board[row-2][col]== "x":
            nums+=1
        elif row < 18 and col < 18 and row > 1 and col > 1 and board[row+2][col+2] =="x" and board[row-2][col-2]== "x":
            nums+=1
    return nums
        
'''Updates the amount of captures player O has from player X'''  
def updateO(board,row,col):
    nums = 0
    if is_capturable(board,row,col, 'x'): 
        if col < 18 and col > 1 and board[row][col+2] == "o" and board[row][col-2] == "o":
            nums+=1
        elif row < 18 and row > 1 and board[row+2][col] =="o" and board[row-2][col] == "o":
            nums+=1
        elif row < 18 and col < 18 and row > 1 and col > 1 and board[row+2][col+2] == "o" and board[row-2][col-2] == "o":
            nums+=1
    return nums
        

@app.route('/')
def main():
    return 'Welcome to a simple 2 Player API implementation of Pente created by Khizar Qureshi & Ntense Obono'


@app.route('/newgame/<player>')
def new_game(player):
    global current 
    current += 1
    gameID = current
    boardSetup = [['-' for i in range(20)] for j in range(20)]
    if player == 'x':
        boardSetup[19//2][19//2] = 'x'
    formatted_board = get_board(boardSetup)
    gameState = 'player:' + player + '#' + 'board:' + formatted_board + '#' + 'capturedX: 0' + '#' + 'capturedO: 0'
    games[gameID] =  {'player': player, 'board': boardSetup, 'capturedX': 0, 'capturedO': 0}
    return json.dumps({'ID':gameID, 'state':gameState})


@app.route('/nextmove/<int:gameID>/<int:row>/<int:col>')
def new_move(gameID, row, col):
    #get states 
    gameState = games[gameID]
    player = gameState.get('player')
    board = gameState.get('board')
    capturedX = gameState.get('capturedX')
    capturedO = gameState.get('capturedO')
    
    #place opponent's spot
    if board[row][col] != '-':
        raise Exception("This spot is already taken!")   
    elif player == 'X' or player == 'x':
        board[row][col] = 'o'  
    else:
        board[row][col] = 'x'

    # place player's spot 
    temp = False
    for rowIndex, row in enumerate(board): 
        for colIndex, col in enumerate(row):
            if col == "-": # pick the first available spot
                board[rowIndex][colIndex] = player 
                myRow, myCol = rowIndex, colIndex
                temp = True
                break
        if temp: break

    
    #loop through the board and check if there are any new captures
    captureX = 0
    captureY = 0
    for rowIndex, row in enumerate(board):
        for colIndex, col in enumerate(row):
            if col == 'o':
                capturedX += updateX(board, rowIndex, colIndex)
            elif col == 'x':
                capturedO += updateO(board, rowIndex, colIndex)
                        
    formatted_board = get_board(board)
    # create new game state
    new_game_state = 'player:' + player + '#' + 'board:' + formatted_board + '#' + 'capturedX:' + str(capturedX) + '#' + 'capturedO:' + str(capturedO)
    #update the dictionary for the game_id
    games[gameID] =  {'player': player, 'board': board, 'capturedX': capturedX, 'capturedO': capturedO}
    return json.dumps({'ID':gameID, 'row':myRow, 'column': myCol, 'gameState': new_game_state})

if __name__ == '__main__':
    parser = argparse.ArgumentParser("Simple Flask application")
    parser.add_argument('host', help = 'the host on which this application is running')
    parser.add_argument('port', type = int, help = 'the port in which this application is listening')
    arguments = parser.parse_args()
    app.run(host = arguments.host, port = arguments.port, debug= True)