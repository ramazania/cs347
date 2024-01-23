import unittest
from frontend.game_logic import *

class TestGameLogic(unittest.TestCase):
    def test_password_generator(self):
        password = password_generator()
        # Check if the password is of the correct length
        self.assertEqual(len(password), max_password_len)
        # Check if all elements of the password are in COLOR_MASTER
        for color in password:
            self.assertIn(color, COLOR_MASTER)

    def test_valid_moves(self):
        # Valid guess
        self.assertTrue(valid_moves("red blue white orange"))
        # Invalid guess (wrong length)
        self.assertFalse(valid_moves("red blue white"))
        # Invalid guess (invalid color)
        self.assertFalse(valid_moves("red blue yellow orange"))

    def test_guess_checker(self):
        # Test when the guess is correct
        password = ["red", "blue", "white", "orange"]
        guess = ["red", "blue", "white", "orange"]
        self.assertTrue(guess_checker(guess, password))

        # Test when the guess has some correct colors in wrong positions
        password = ["red", "blue", "white", "orange"]
        guess = ["orange", "white", "blue", "red"]
        self.assertFalse(guess_checker(guess, password))

        # Test when the guess is completely wrong
        password = ["red", "blue", "white", "orange"]
        guess = ["purple", "magenta", "green", "yellow"]
        self.assertFalse(guess_checker(guess, password))

if __name__ == '__main__':
    unittest.main()
