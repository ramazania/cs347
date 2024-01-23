from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import random
import mysql.connector
import game_logic

app = Flask(__name__, 
        static_url_path='/static',
        static_folder='static',
        template_folder='templates')

game_id = ''
for i in range(15):
    game_id += str(random.randint(0, 9))

app.config['SESSION_TYPE'] = 'filesystem'

app.secret_key = game_id

# loads the home page
@app.route('/')
@app.route('/home')
def home():
    print("In HOME page")
    return render_template('home.html')

# loads the "how to play" page for general game rules and instructions
@app.route('/howtoplay')
def howtoplay():
    return render_template('howtoplay.html')

# loads game creation page, for starting a new game or continuing an unfinished game
@app.route('/pregame')
def pregame():
    return render_template('pregame.html')

# Loads the game page, for playing a unique game of Mastermind
@app.route('/game')
def game():
    print("In GAME page")
    game_logic.reset_game()
    return render_template('game.html')

# This loads a test page to make sure the HTML form of the player's guess
# is correct and can be parsed for the game logic
@app.route('/update', methods = ['GET'])
def update():
    playerguess = []
    num = 1
    for i in request.args:
        playerguess.append(request.args.get("color" + str(num)))
        num += 1

    result = ','.join(playerguess)

    # Establish a connection to the database
    cnx = mysql.connector.connect(user='webapp', password='masterminds1', host='db', database='MasterMinds')
    cursor = cnx.cursor(buffered=True)

    # Fetch the current moves for the player using their game ID (modify this based on your actual game logic)
    # Replace with the actual game ID
    cursor.execute("SELECT moves FROM PlayerData WHERE gameID = %s", (game_id,))
    existing_moves = cursor.fetchone()[0]  # Fetch the existing moves

    # Combine the existing moves with the new moves separated by a semicolon
    new_moves = existing_moves + ';' + result if existing_moves else result

    # Update moves column in the database for the specific game ID
    update_query = "UPDATE PlayerData SET moves = %s WHERE gameID = %s"
    cursor.execute(update_query, (new_moves, game_id))
    cnx.commit()

    # Close database connection
    cursor.close()
    cnx.close()
    cur_game = game_logic.guess_checker(playerguess)
    if (cur_game['isComplete'] > 0):
        session['data'] = cur_game
        att = cur_game['attempts']
        cnx = mysql.connector.connect(user='webapp', password='masterminds1', host='db', database='MasterMinds')
        cursor = cnx.cursor(buffered=True)

        update_query = "UPDATE PlayerData SET attempts = %s WHERE gameID = %s"
        finish_query = "UPDATE PlayerData SET gameComplete = %s WHERE gameID = %s"

        cursor.execute(update_query, (att, game_id))
        cnx.commit()

        cursor.execute(finish_query, (cur_game['isComplete'], game_id))
        cnx.commit()

        # Close database connection
        cursor.close()
        cnx.close()
    return jsonify(cur_game)
 
# Takes the player's results and displays them    
@app.route('/gamecomplete')
def gamecomplete():
    game_info = session['data']
    attempts = game_info['attempts']
    masterPass = game_info['masterPass']
    gameState = game_info['isComplete']
    return render_template('results.html', 
                           attempts=attempts, masterPass=masterPass, gameState=gameState)

# Retrieves data about each player from the DB, transforms it into a readable format and renders the scoreboard page
# Implemented by Aidan Roessler from team Vaas
@app.route('/scoreboard')
def scoreboard():
    # TODO Rotate password and store in an environment variable to not expose it to the FE
    cnx = mysql.connector.connect(user='webapp', password='masterminds1', host='db', database='MasterMinds')
    cursor = cnx.cursor(buffered=True)
    
    query = "SELECT name, gameID, attempts FROM PlayerData WHERE gameComplete = TRUE"
    
    cursor.execute(query) 

    cnx.commit()

    results = cursor.fetchall()
    columns = cursor.column_names
    
    # Create a list of dictionaries where in each dictionary each key corresponds
    # to a column, (eg. Name) and each value for that key is the value for that row 
    list_of_players = []
    for row in results:
        row_dict = {}
        for i in range(len(columns)):
            column_name = columns[i]
            column_value = row[i]
            row_dict[column_name] = column_value
        list_of_players.append(row_dict)  

    cursor.close()
    cnx.close()

    return render_template('scoreboard.html', list_of_players = list_of_players)

@app.route('/insert', methods=['POST'])  
def insert():
    game_logic.reset_game()
    global game_id
    # Retrieve player name from the form
    
    form_data = request.form
    player_name = form_data['player']

    # Establish connection to the database
    cnx = mysql.connector.connect(user='webapp', password='masterminds1', host='db', database='MasterMinds')
    cursor = cnx.cursor(buffered=True)

    # Prepare SQL query (use parameterized query to avoid SQL injection)
    query = "INSERT INTO PlayerData (name) VALUES (%s)"
    data = (player_name,)  # Data tuple

    # Execute query
    cursor.execute(query, data)
    cnx.commit()

    # Retrieve the last inserted ID (gameID)
    cursor.execute("SELECT LAST_INSERT_ID()")
    last_game_id = cursor.fetchone()[0]  # Fetch the last inserted gameID

    # Store the retrieved gameID in the global variable
    game_id = last_game_id

    # Close database connection
    cursor.close()
    cnx.close()

    # Return a response to the user
    return render_template('game.html', player=player_name, game_id=game_id)

@app.route('/lookup')
def direct_form():
    return render_template('lookup.html')

@app.route('/player', methods = ['POST'])
def lookup():
    cnx = mysql.connector.connect(user='webapp', password='masterminds1', host='db', database='MasterMinds')
    cursor = cnx.cursor(buffered=True)
    form_data = request.form
    player_id = form_data['name']
    
    query = "SELECT name, gameID, moves, attempts, gameComplete FROM PlayerData WHERE gameID = '" + player_id + "'";
    
    cursor.execute(query) 
    cnx.commit()
    output_str = ""
    for data in cursor:
        for item in data:
            output_str = output_str + str(item) + ",   "
        output_str = output_str + "\n"

    return render_template('player.html', output =output_str)

app.run(host='0.0.0.0', port=5500)