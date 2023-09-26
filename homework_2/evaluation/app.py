import requests
from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route('/')
def hello():
    # response = requests.get('http://localhost:7555/')
    # jsonResponse = response.json()
    # num = jsonResponse['rand'];    
    return "hello world"

if __name__ == '__main__':
    app.run(port=5000)