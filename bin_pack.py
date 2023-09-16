from flask import Flask, jsonify, session
import json
import argparse
import random

app = Flask(__name__)

app.secret_key = b'suieoNII902883094u___123$'

def random_num_gen():
    while True:
        num = ""
        for i in range(6):
            num += str(random.randint(0, 9))
        num = int(num)

        if num not in session['problemIDs']:
            session['problemIDs'].append(num)
            session['problems'].append([num, '####', []])
            break
    return int(num)

def checksession():
    if 'problemIDs' not in session:
        session['problemIDs'] = []
    if 'problems' not in session:
        session['problems'] = []

def checkID(problemID):
    if problemID not in session['problemIDs']:
        return False
    print(session['problems'])
    for problem in session['problems']:
        print(problem)
        if problem[0] == problemID:
            return problem


@app.route("/newproblem")
def newproblem():
    checksession()
    ID = random_num_gen()
    res = {
        'ID': ID,
        'bins': '####',
    }
    return jsonify(res)


@app.route('/placeitem/<problemID>/<size>')
def placeitem(problemID, size):
    checksession()
    problem = checkID(problemID)
    if not problem:
        return "Invalid problem ID"


    res = {
        'ID': problem[0],
        'size': size,
        'loc': 932,
        'bins': problem[2]
    }

    # updateProblem()

    return jsonify(res)
    


if __name__ == '__main__':
    parser = argparse.ArgumentParser('A sample Flask application/API')
    parser.add_argument('host', help='the host on which this application is running')
    parser.add_argument('port', type=int, help='the port on which this application is listening')
    arguments = parser.parse_args()
    app.run(host=arguments.host, port=arguments.port, debug=True)