from flask import Flask, jsonify, session
import json
import argparse
import random

app = Flask(__name__)

num = ''
for i in range(15):
    num += str(random.randint(0, 9))

app.config['SESSION_TYPE'] = 'filesystem'

app.secret_key = num

def random_num_gen():
    while True:
        num = ""
        for i in range(6):
            num += str(random.randint(0, 9))
        num = int(num)

        session['problemIDs'].append(num)
        session['problems'].append([num, '####', [100]])
        return num

def checksession():
    if 'problemIDs' not in session:
        session['problemIDs'] = []
    if 'problems' not in session:
        session['problems'] = []

def checkID(problemID):
    print("current problem ID", problemID)
    print("Current problemIDS in session", session['problems'])
 
    for problem in session['problems']:
        if int(problem[0]) == int(problemID):
            return problem
    return False

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
    problem = checkID(problemID)
    if not problem:
        return "Invalid problem ID"
    
    bins = problem[2]
    placed = False

    for index, bin in enumerate(bins):
        if int(bin) > int(size):
            bins[index] = int(bin) - int(size)
            placed = True
            
    encoding = problem[1].replace('##','')
    encoding = encoding.split('#')

    if not placed:
        bins.append(100-int(size))
        encoding.append('')
        index += 1
    
    if len(encoding[index]) == 0:
        encoding[index] = str(size)
    else:
        encoding[index] += '!' + str(size)

    encoding = '#'.join(encoding)

    encoding = '##' + encoding + '##'

    problem[1] = encoding

    allProblems = session['problems']

    for index, oldProblem in enumerate(allProblems):
        if int(oldProblem[0]) == problemID:
            allProblems[index] = problem
    
    session['problems'] = allProblems

    res = {
        'ID': problem[0],
        'size': size,
        'loc':index + 1,
        'bins': problem[1]
    }

    return jsonify(res)

@app.route('/endproblem/<problemID>')
def endproblem(problemID):
    problem = checkID(problemID)
    if not problem:
        return "Invalid problem ID"

    encoding = problem[1].replace('##','')
    bins = encoding.split('#')
   
    total_size = 0
    for bin in bins:
        if '!' in bin:
            bin = bin.split('!')
            for item in bin:
                total_size += int(item)
        else:
            total_size += int(bin)
    
      
    num_items = 0
    for bin in bins:
        bin = bin.split('!')
        num_items += len(bin)

    num_bins = len(bins)
    total_capacity = num_bins * 100
    wasted_space = total_capacity - total_size
    
    end = {
        'ID': problem[0],
        'size': total_size,
        'items': num_items,
        'count': num_bins,
        'wasted': wasted_space,
        'bins': problem[1]
    }

    return jsonify(end)
    


if __name__ == '__main__':
    parser = argparse.ArgumentParser('A sample Flask application/API')
    parser.add_argument('host', help='the host on which this application is running')
    parser.add_argument('port', type=int, help='the port on which this application is listening')
    arguments = parser.parse_args()
    app.run(host=arguments.host, port=arguments.port, debug=True)