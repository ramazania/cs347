import requests
from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route('/')
def hello():
    response = requests.get('http://homework_2:5000/newgame/x')
    jsonResponse = response.json()    
    return jsonResponse

if __name__ == '__main__':
    app.run(port=5000)
