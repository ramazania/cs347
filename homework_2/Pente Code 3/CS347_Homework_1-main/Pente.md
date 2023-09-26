You are to code an API for the two-player game of Pente. In essence your API will be providing an AI player that makes moves in Pente. 
You need not make intelligent moves, but you must make legal moves.

You can find information about the game at the following links:
- [Wikipedia Page](https://en.wikipedia.org/wiki/Pente)
- [Rules Document](https://www.ultraboardgames.com/pente/game-rules.php)

---

## Board Encoding

The two players are denoted X and O. Player X is the player who moves first. Blank squares are denoted by the dash character \-

The state of the game is encoded as a string with the following format:

  player#board#capturedX#capturedO

The components of the game state are as follows:
- **player** is a single character (either X or O) indicating who is the next player to place a stone
- **board** is a string of 361 characters (one for each space of the board) indicating which piece is on each square. Each character should be X, O or dash.
- The first 19 characters represent the first row of the board, the second 19 characters represent the second row, and so forth ...
- **capturedX** indicates the number of stones (originally belonging to O) that have been captured by the X player.
- **capturedY** indicates the number of stones (originally belonging to X) that have been captured by the O player.

## API Endpoint - New Game

Your API is essentially implementing a simple AI for the Pente game. You are NOT asked to make good moves, but you must make legal moves.

/newgame/player

Input: **player** is either X or O indicating whether your AI is playing as X or as O

Output is a JSON Object:

  {
  'ID': gameID
  'state' : gamestate
  }

The **gameID** should be an integer that can be used to reference a particular game. (Each gameID should be unique)

The **gamestate** If you are player O then the game state should be an empty board (waiting for your opponent to move). 
If you are player X, then the gamestate should have a single X piece on the board in the location of your player's first move

## API Endpoint - Next Move

/nextmove/gameID/row/col

Input: 
-- **gameID** is the unique ID that was associated with the game when it was created. 
-- **row** is the row in which your opponent placed their piece
-- **col** is the column in which your opponent placed their piece

You should update the gamestate for the given gameID to add your opponent's newest piece at location row, col. Then your AI player should make a legal move.

Output is a JSON Object:

  {
  'ID': gameID
  'row': myRow
  'column': myCol
  'state' : new_gamestate
  }

The **gameID** should be the same as was provided in the input

**myRow** and **myCol** should be the row and column where your AI player just placed a piece.

The **gamestate** should be the new state of the game incorporating both your opponent's move and your latest move.

## Submission

You should create a GitHub repository that includes your code. Please make your code as clear and easy to read as possible. 

It would be helpful to include some test cases. I have provided skeleton test code that might be useful.


