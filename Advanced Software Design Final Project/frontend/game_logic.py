import random

COLOR_MASTER = ['red', 'blue', 'saddlebrown', 'pink', 'purple', 'green']

max_password_len = 4
max_password_attempts = 8
allow_repeats = False
attempts = 0

#Creates a randomized list of colors to act as the game's password
def password_generator():
    if not (allow_repeats):
        password = random.sample(COLOR_MASTER, max_password_len)
    else:
        for i in range(max_password_len):
            color = random.choice(COLOR_MASTER)
            if (color in password) and (password.count(color) <= 2):
                password.append(color)

    return password

#Makes sure user's guess is the right length and has viable colors    
def valid_moves(user_guess: str):
    if len(user_guess) != max_password_len:
        return False
    for color in user_guess:
        if color.lower() not in COLOR_MASTER:
            return False
    return True

# Parses the user's guess to see what they got correct. 
# Prints out relevant information and returns false if there are any incorrect guesses
def guess_checker(user_guess):
    global master_password, attempts
    attempts += 1
    print("user: ", user_guess)
    print("answer: ", master_password)
    guess = user_guess
    correct = 0 # for 'red' hints, meaning the player has a color from the master password in the correct position
    false_position = 0 # for 'white' hints, meaning the player has a color from the master password in the wrong position
    empty = 0
    isComplete = 0 # 0 if not done, 1 if player won, 2 if player lost
    for i in range(max_password_len):
        if(guess[i] == master_password[i]):
            correct += 1
        else:
            if(guess[i] in master_password):
                false_position += 1
            else:
                empty += 1
    
    if (correct == max_password_len):
        isComplete = 1
    elif (attempts == max_password_attempts):
        isComplete = 2
    res = {
        'red': correct,
        'white': false_position,
        'attempts' : attempts,
        'guess' : guess,
        'isComplete' : isComplete,
        'masterPass' : master_password
    }
    return res

def reset_game():
    global master_password, attempts
    attempts = 0
    master_password = password_generator()