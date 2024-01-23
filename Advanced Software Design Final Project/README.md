# cs347-final

## Authors: 	
		Ali Ramazani, 
		Barry Nwike, 
		Peyton Bass, 
		Muno Siyakurima


## Description:

Final Project for CS347 class implemented by Ali Ramazani, Barry Nwike, Peyton Bass and Muno Siyakurima.
Project is a web implementation of the Mastermind Game making use of Docker containers and databases.

We only have two containers:
1. db: managing the database
2. frontend: includes the game logic, python flask, and webapp.py

## How to run our project:
1. Open Docker
2. If the db-storage folder is not empty, make sure to delete the db-storage folder and recreate it. It should be empty for the code to run correctly on your local machine.
3. Run docker compose up in your terminal
4. The link to our game web page is in the frontend container

## Pregame Page:
When you click on the "Play" tab under navigation, you will be asked to enter your name. Make
sure your name DOES NOT include spaces, else the website will return an error

## Game Hint Explanation:
1. Red: represents the number of correct colors in the correct position
2. White: represents the number of correct colors in the wrong position

## Player Page Explanation:
When you look up a player to see their stats, you will see:
1. Name: player name
2. Game ID: a unique number
3. Moves: contains four colors per each move, which is separated by a semicolon. 
4. Attempts: the number of tries
5. Game Complete: 0 means in progress, 1 means the player won, and 2 means the player lost.


## Stats Page Explanation:
The Vaas team created the stats page for our project. They made the following files:
1. HTML Page: scoreboard.html
2. scoreboard function in the webapp.py: Implemented by Aidan Roessler from team Vaas
