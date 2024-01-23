
class GameBoard:
    def __init__(self, spaces, rows):
        self.spaces = spaces
        self.rows = rows
        self.board = []
        self.index = 0
        self.generate_board()
    
    #creates a board with a bunch of empty spaces
    def generate_board(self):
        board = ""
        for i in range(0, self.rows):
            board += "|" + (" x " * self.spaces) + "|"
            board += "/"

        self.board = board.split("/")
    
    #updates the newest line of the board based on the user's input
    def update_board(self, turn: int, input):
        answer = input
        line = ""
        for color in answer:
            line += " " + color[0] + " "

        self.board[turn] = "|" + line + "|"
    
    #prints out the board line by line
    def display_board(self):
        for row in self.board:
            print(row)


def main():
    boardgame = GameBoard(4, 6)
    boardgame.generate_board()
    print(boardgame.rows)
    boardgame.update_board(0, "red blue black orange")

    for row in boardgame.board:
        print(row)

if __name__ == "__main__": 
    main() 