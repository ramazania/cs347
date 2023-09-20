import flask
import json
import argparse
import sys
import datetime
import random

app = flask.Flask(__name__)

# ---------------

games_dict = {}
games_remaining_moves_dict = {}

# ---------------

def unique_id_generator():
    """
    DESCRIPTION:
        Generate a unique ID (for each game session)
        The idea is simple, convert the current datetime.now() into an integer

    OUTPUT SIGNATURE:
        1. unique_id (str): the unique ID
    """
    
    # get current time
    now = datetime.datetime.now()

    # convert to timestamp (seconds since 1970)
    now_float = now.timestamp()

    # convert to a unique integer
    now_int = int(now_float * 10**6)

    # string convert it to avoid scientific notation display
    now_str = str(now_int)

    return now_str

@app.route("/newgame/<str:player>")
def create_new_game(player):

    player = player
    game_id = unique_id_generator()

    # generate board
    one_row = "-------------------"
    board = one_row * 19

    # make a random move if player is X
    if player == "X":
        random_move = random.randint(0, 360)
        board[random_move] = "X"
    
    # update gamestate
    gamestate = player + "#" + board +"#" + str(0) + "#" + str(0)
    games_dict[game_id] = gamestate

    # update remaining moves
    remaining_moves = set(range(0, 360))
    games_remaining_moves_dict[game_id] = remaining_moves

    # return game jason object
    game = {
        "game_id" : game_id,
        "gamestate" : gamestate
    }
    
    return json.dumps(game)


def legal_move_checker(game_id, move):
    board = games_dict[game_id].split("#")[1]
    if(board[move]) == "-":
        return True
    else:
        return False

@app.route("/nextmove/gameID/row/col")
def nextMove(gameID, row, col):

    previous_move = row * 19 + col - 1 # row and col starts from 1

    # remove the previous move from remaining moves
    remaining_moves = games_remaining_moves_dict[gameID]
    remaining_moves.remove(previous_move)
    games_remaining_moves_dict[gameID] = remaining_moves
    
    # make the next move and update the database
    next_move = random.choice(remaining_moves)
    remaining_moves.remove(next_move)
    games_remaining_moves_dict[gameID] = remaining_moves
    next_col = index_to_col(next_move)
    next_row = index_to_row(next_move)

    # update gamestate
    previous_state = games_dict[gameID]
    previous_player = previous_state.split("#")[0]

    if previous_player == "X":
        new_player = "O"
    else:
        new_player = "X"

    next_board = previous_state.split("#")[1]
    next_board[next_move] = new_player

    # check capture
    check_capture(gameID, new_player, next_col, next_row) # game state is updated WITHIN this function
    new_gamestate = games_dict[gameID]

    data = {
        'ID': gameID,
        'row': next_row,
        'column': next_col,
        'state' : new_gamestate

    }
    return json.dumps(data)

def index_to_col(index):
    # index is a number from 0 to 360 specifying which square of the board it is
    return (index + 1) % 19 # column starts from 1

def index_to_row(index):
    # index is a number from 0 to 360 specifying which square of the board it is
    return (index + 1) // 19 + 1 # row starts from 1

def col_row_to_index(col, row):
    # col and row starts from 1
    return (row - 1) * 19 + col - 1

def check_capture(gameID, player, next_col, next_row):

    check_capture_horizontal(gameID, player, next_col, next_row)
    check_capture_vertical(gameID, player, next_col, next_row)
    check_capture_diagonal_positive_slope(gameID, player, next_col, next_row)
    check_capture_diagonal_negative_slope(gameID, player, next_col, next_row)

def check_capture_horizontal(gameID, player, next_col, next_row):
    
    state = games_dict[gameID]
    board = state.split("#")[1]

    if player == "X":
        opponent = "O"
    else:
        opponent = "X"

    # check capture horizontal right
    if next_col <= 16:

        end_capture_point = col_row_to_index(next_col + 3, next_row)

        if board[end_capture_point] == player:

            capturing_location_1 = col_row_to_index(next_col + 1, next_row)
            capturing_location_2 = col_row_to_index(next_col + 2, next_row)

            if board[capturing_location_1] == opponent and board[capturing_location_2] == opponent:
                
                # adjust the board and state
                board[capturing_location_1] = "-"
                board[capturing_location_2] = "-"

                if opponent == "X":
                    new_X_captured = int(state.split("#")[2]) + 2
                    new_O_captured = int(state.split("#")[3])

                else:
                    new_X_captured = int(state.split("#")[2])
                    new_O_captured = int(state.split("#")[3]) + 2

                state = player + "#" + board + "#" + str(new_X_captured) + "#" + str(new_O_captured)

    # check capture horizontal left
    if next_col >= 4:

        end_capture_point = col_row_to_index(next_col - 3, next_row)

        if board[end_capture_point] == player:

            capturing_location_1 = col_row_to_index(next_col - 1, next_row)
            capturing_location_2 = col_row_to_index(next_col - 2, next_row)

            if board[capturing_location_1] == opponent and board[capturing_location_2] == opponent:
                
                # adjust the board and state
                board[capturing_location_1] = "-"
                board[capturing_location_2] = "-"

                if opponent == "X":
                    new_X_captured = int(state.split("#")[2]) + 2
                    new_O_captured = int(state.split("#")[3])

                else:
                    new_X_captured = int(state.split("#")[2])
                    new_O_captured = int(state.split("#")[3]) + 2

                state = player + "#" + board + "#" + str(new_X_captured) + "#" + str(new_O_captured)

    # update state in the database
    games_dict[gameID] = state

def check_capture_vertical(gameID, player, next_col, next_row):
    
    state = games_dict[gameID]
    board = state.split("#")[1]

    if player == "X":
        opponent = "O"
    else:
        opponent = "X"

    # check capture downwards
    if next_row <= 16:

        end_capture_point = col_row_to_index(next_col, next_row + 3)

        if board[end_capture_point] == player:

            capturing_location_1 = col_row_to_index(next_col, next_row + 1)
            capturing_location_2 = col_row_to_index(next_col, next_row + 2)

            if board[capturing_location_1] == opponent and board[capturing_location_2] == opponent:
                
                # adjust the board and state
                board[capturing_location_1] = "-"
                board[capturing_location_2] = "-"

                if opponent == "X":
                    new_X_captured = int(state.split("#")[2]) + 2
                    new_O_captured = int(state.split("#")[3])

                else:
                    new_X_captured = int(state.split("#")[2])
                    new_O_captured = int(state.split("#")[3]) + 2

                state = player + "#" + board + "#" + str(new_X_captured) + "#" + str(new_O_captured)

    # check capture upwards
    if next_col >= 4:

        end_capture_point = col_row_to_index(next_col, next_row - 3)

        if board[end_capture_point] == player:

            capturing_location_1 = col_row_to_index(next_col, next_row - 1)
            capturing_location_2 = col_row_to_index(next_col, next_row - 2)

            if board[capturing_location_1] == opponent and board[capturing_location_2] == opponent:
                
                # adjust the board and state
                board[capturing_location_1] = "-"
                board[capturing_location_2] = "-"

                if opponent == "X":
                    new_X_captured = int(state.split("#")[2]) + 2
                    new_O_captured = int(state.split("#")[3])

                else:
                    new_X_captured = int(state.split("#")[2])
                    new_O_captured = int(state.split("#")[3]) + 2

                state = player + "#" + board + "#" + str(new_X_captured) + "#" + str(new_O_captured)

    # update state in the database
    games_dict[gameID] = state

def check_capture_diagonal_positive_slope(gameID, player, next_col, next_row):
    """
    Positive slope means the diagonal is like this /
    """
    
    state = games_dict[gameID]
    board = state.split("#")[1]

    if player == "X":
        opponent = "O"
    else:
        opponent = "X"

    # check capture diagonal upward
    if next_col <= 16 and next_row >= 4:

        end_capture_point = col_row_to_index(next_col + 3, next_row + 3)

        if board[end_capture_point] == player:

            capturing_location_1 = col_row_to_index(next_col + 1, next_row - 1)
            capturing_location_2 = col_row_to_index(next_col + 2, next_row - 2)

            if board[capturing_location_1] == opponent and board[capturing_location_2] == opponent:
                
                # adjust the board and state
                board[capturing_location_1] = "-"
                board[capturing_location_2] = "-"

                if opponent == "X":
                    new_X_captured = int(state.split("#")[2]) + 2
                    new_O_captured = int(state.split("#")[3])

                else:
                    new_X_captured = int(state.split("#")[2])
                    new_O_captured = int(state.split("#")[3]) + 2

                state = player + "#" + board + "#" + str(new_X_captured) + "#" + str(new_O_captured)

    # check capture diagonal downward
    if next_col >= 4 and next_row >= 16:

        end_capture_point = col_row_to_index(next_col - 3, next_row - 3)

        if board[end_capture_point] == player:

            capturing_location_1 = col_row_to_index(next_col - 1, next_row + 1)
            capturing_location_2 = col_row_to_index(next_col - 2, next_row + 2)

            if board[capturing_location_1] == opponent and board[capturing_location_2] == opponent:
                
                # adjust the board and state
                board[capturing_location_1] = "-"
                board[capturing_location_2] = "-"

                if opponent == "X":
                    new_X_captured = int(state.split("#")[2]) + 2
                    new_O_captured = int(state.split("#")[3])

                else:
                    new_X_captured = int(state.split("#")[2])
                    new_O_captured = int(state.split("#")[3]) + 2

                state = player + "#" + board + "#" + str(new_X_captured) + "#" + str(new_O_captured)

    # update state in the database
    games_dict[gameID] = state

def check_capture_diagonal_negative_slope(gameID, player, next_col, next_row):
    """
    Positive slope means the diagonal is like this \
    """
    
    state = games_dict[gameID]
    board = state.split("#")[1]

    if player == "X":
        opponent = "O"
    else:
        opponent = "X"

    # check capture diagonal upward
    if next_col >= 4 and next_row >= 4:

        end_capture_point = col_row_to_index(next_col - 3, next_row - 3)

        if board[end_capture_point] == player:

            capturing_location_1 = col_row_to_index(next_col - 1, next_row - 1)
            capturing_location_2 = col_row_to_index(next_col - 2, next_row - 2)

            if board[capturing_location_1] == opponent and board[capturing_location_2] == opponent:
                
                # adjust the board and state
                board[capturing_location_1] = "-"
                board[capturing_location_2] = "-"

                if opponent == "X":
                    new_X_captured = int(state.split("#")[2]) + 2
                    new_O_captured = int(state.split("#")[3])

                else:
                    new_X_captured = int(state.split("#")[2])
                    new_O_captured = int(state.split("#")[3]) + 2

                state = player + "#" + board + "#" + str(new_X_captured) + "#" + str(new_O_captured)

    # check capture diagonal downward
    if next_col <= 16 and next_row <= 16:

        end_capture_point = col_row_to_index(next_col + 3, next_row + 3)

        if board[end_capture_point] == player:

            capturing_location_1 = col_row_to_index(next_col + 1, next_row + 1)
            capturing_location_2 = col_row_to_index(next_col + 2, next_row + 2)

            if board[capturing_location_1] == opponent and board[capturing_location_2] == opponent:
                
                # adjust the board and state
                board[capturing_location_1] = "-"
                board[capturing_location_2] = "-"

                if opponent == "X":
                    new_X_captured = int(state.split("#")[2]) + 2
                    new_O_captured = int(state.split("#")[3])

                else:
                    new_X_captured = int(state.split("#")[2])
                    new_O_captured = int(state.split("#")[3]) + 2

                state = player + "#" + board + "#" + str(new_X_captured) + "#" + str(new_O_captured)

    # update state in the database
    games_dict[gameID] = state