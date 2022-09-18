# The example function below keeps track of the opponent's history and plays whatever the opponent played two plays ago. It is not a very good player so you will need to change the code to pass the challenge.
import numpy as np

ideal_response = {"P": "S", "R": "P", "S": "R"}
my_moves = ["R"]
opponent_history = []
strategy = [0, 0, 0, 0]
opponent_guess = ["", "", "", ""] #
strategy_guess = ["", "", "", ""]
opponent_play_order = {}
my_play_order = {}


def player(prev_play):
    # if 2nd game or more, add/append in the list opponent history
    if prev_play in ["R", "P", "S"]:
        opponent_history.append(prev_play)
        # 'i' will return
        for i in range(0, 4):
            if opponent_guess[i] == prev_play:
                strategy[i] += 1
    # if there's a new player, game will reset
    else:
        reset()

    # get latest 10 moves
    my_last_ten = my_moves[-10:]
    # if the latest 10 moves already have input
    if len(my_last_ten) > 0:
        # most frequent move
        my_most_frequent_move = max(set(my_last_ten), key=my_last_ten.count)
        # the opponent will beat my most frequent move
        opponent_guess[0] = ideal_response[my_most_frequent_move]
        # to beat the opponent, my guess is to guess line 33 then change my move
        strategy_guess[0] = ideal_response[opponent_guess[0]]

    # if the game length is below 10
    if len(my_moves) > 0:
        # get the last play
        my_last_play = my_moves[-1]
        # the opponent will beat the latest play
        opponent_guess[1] = ideal_response[my_last_play]
        # to beat opp, my guess is to guess line 42
        strategy_guess[1] = ideal_response[opponent_guess[1]]

    # with at least 3 games (opponent_history)
    if len(opponent_history) >= 3:
        
        opponent_guess[2] = predict_move(opponent_history, 3, opponent_play_order)
        # whatever is predicted
        strategy_guess[2] = ideal_response[opponent_guess[2]]

    # with atleast 2 games (my_moves)
    if len(my_moves) >= 2:
        # reverse guess from line 51
        opponent_guess[3] = ideal_response[predict_move(my_moves, 2, my_play_order)]
        # reverse guess line 56
        strategy_guess[3] = ideal_response[opponent_guess[3]]

    # get the most frequent strategy
    best_strategy = np.argmax(strategy)
    # the guess with the best_strategy
    guess = strategy_guess[best_strategy]
    # scissors default move 
    if guess == "":
        guess = "S"
    # records the move
    my_moves.append(guess)
    return guess


def predict_move(history, n, play_order):
    # records the player history

    # if with history, add 1 to the count
    if "".join(history[-n:]) in play_order.keys():
        play_order["".join(history[-n:])] += 1

    # if no history, define new/next move of the opponent
    else:
        play_order["".join(history[-n:])] = 1
    #example scenario below:
    # RRP
    # RP
    # RPR, RPP, RPS
    possible = ["".join(history[-(n - 1) :]) + k for k in ["R", "P", "S"]]
    # in the possibilities, check if within play order list
    for pm in possible:
        # if not in play order list, mark as 0
        if not pm in play_order.keys():
            play_order[pm] = 0

    # most number of counts of possibilities in play order list
    predict = max(possible, key=lambda key: play_order[key])
    return predict[-1]


def reset():
    global my_moves, opponent_history, strategy, opponent_guess, strategy_guess, opponent_play_order, my_play_order
    my_moves = ["R"]
    opponent_history.clear()
    strategy = [0, 0, 0, 0]
    opponent_guess = ["", "", "", ""]
    strategy_guess = ["", "", "", ""]
    opponent_play_order = {}
    my_play_order = {}

