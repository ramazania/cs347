import json
import requests
from flask import Flask
from flask import render_template

app = Flask(__name__)


def playGame(id):
    col = 3
    row = 1

    while True:

        row += 1
        res = requests.get(f'http://api:5000//nextmove/{id}/{col}/{row}')

        print(res)
        print(res.content)
        
        if res.text == 'x won' or res.text == 'o won':
            # print(res.content)
            print("O HAS OWN THE GAME")
            return "O has won the game"
    

@app.route('/')
def startGame():

    res = requests.get('http://api:5000/newgame/o')   
    if res.status_code != 200:
        print("Game couldn't be started")

    else:
        json_data = res.json()
        id = json_data['ID']

        print(f"Game is running with ID {id}")
        res = playGame(id)
        return res


if __name__ == '__main__':
    app.run(port=5000)

