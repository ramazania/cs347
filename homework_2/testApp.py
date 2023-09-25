import unittest
import flask
import app
import json

class AppTest(unittest.TestCase):

    def test_create_new_game_type(self):
        """
        DESCRIPTION:
            Checks if the new game created is the proper type (string type)
        OUTPUT:
            Pass if the a string type, fail otherwise
        """
        game = app.create_new_game('X')
        self.assertEqual(type(game), str, 'Does not return a JSON string')

    def test_create_new_game_ID(self):
        """
        DESCRIPTION:
            Checks if the new game has a unique gameID compared to another new game
        OUTPUT:
            Pass if the gameIDs are unique, fail otherwise
        """
        gameOne = app.create_new_game('X')
        gameTwo = app.create_new_game('X')
        self.assertNotEqual(json.loads(gameOne)["game_id"], json.loads(gameTwo)["game_id"], 'Games do not have unique gameIDs')

    def test_create_new_game_state_X(self):
        """
        DESCRIPTION:
            Checks if the new game has a single X piece when the starting player is X
        OUTPUT:
            Pass if the board contains in X, fail otherwise
        """
        game = app.create_new_game('X')
        board = json.loads(game)["gamestate"].split("#")[1]
        self.assertIn('X', board, 'There is no X in the board')

    def test_create_new_game_state_O_One(self):
        """
        DESCRIPTION:
            Checks if the new game has an empty board (No Xs) when the starting player is O
        OUTPUT:
            Pass if the board contains nothing, fail otherwise
        """
        game = app.create_new_game('O')
        board = json.loads(game)["gamestate"].split("#")[1]
        self.assertNotIn('X', board, 'The board contains in X and is not empty')

    def test_create_new_game_state_O_Two(self):
        """
        DESCRIPTION:
            Checks if the new game has an empty board (No Os) when the starting player is O
        OUTPUT:
            Pass if the board contains nothing, fail otherwise
        """
        game = app.create_new_game('O')
        board = json.loads(game)["gamestate"].split("#")[1]
        self.assertNotIn('O', board, 'The board is contains an O and is not empty')

    def test_check_legal_move(self):
        """
        DESCRIPTION:
            Checks if a legal move is detected
        OUTPUT:
            Pass if assertion is True, fail otherwise
        """
        exampleBoard = "X------------------"
        self.assertTrue(app.legal_move_checker("X#" + exampleBoard + "#1#0", 1), 'Player did not make a legal move')

    def test_check_illegal_move(self):
        """
        DESCRIPTION:
            Checks if an illegal move is detected
        OUTPUT:
            Pass if assertion is False, fail otherwise
        """
        exampleBoard = "X------------------"
        self.assertFalse(app.legal_move_checker("X#" + exampleBoard + "#1#0", 0), 'Player did not make a illegal move')

    def test_nextMove_gamestate(self):
        """
        DESCRIPTION:
            Checks if the gamestate has changed since a move was made
        OUTPUT:
            Pass if assertion is False, fail otherwise
        """
        pente = app
        newgame = pente.create_new_game('X')
        newgameID = json.load(newgame)["game_id"]
        newgame_currentstate = json.load(newgame)["gamestate"]

        new_move = pente.nextMove(newgameID, 2, 2)
        newgame_newstate = json.load(new_move)["state"]

        self.assertNotEqual(newgame_currentstate, newgame_newstate, 'Gamestate has not chanaged since newest move was made')

if __name__ == "__main__":
    unittest.main()