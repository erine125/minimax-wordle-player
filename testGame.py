import random
from wordle import Wordle, filter_wordlist, word_consistent, generate_feedback

def play_game_manual(guesses_list, soln_list, player):
    """
    Plays the game manually. Takes in a list of possible guesses and a list of possible solutions,
    as well as the type of player to use ("minimax" or "random").
    """
    game = Wordle(guesses_list, soln_list)

    print("--------------")
    print("Turn num:", game.turn_num)
    game.makeMoveManual('arise')
    # When given NO info, program chooses 'arise', i.e. it's the best
    # word to guess when we have no info.
    # since we always have no info to start with, we can just hard code this in as the starting word.
    # if using a different word list, or you want the player to compute its own starting word,
    # simply comment out the above lines.

    while not game.isTerminal:
        print("--------------")
        print("Turn num:", game.turn_num)
        if player == "random":
            move = game.greedyRandomSelect()
        elif player == "minimax":
            move = game.minimaxSelect()
        else:
            print("Please choose 'minimax' or 'random' player.")
            exit()

        if move == None:
            print("Solver failed. Double check feedback!")
            break

        game.makeMoveManual(move)

    if len(game.green_pairs) == 5:
        print("--------------")
        print("Guessed word in %d turns" % (game.turn_num-1))
        print()

def play_game_automatic(guesses_list, soln_list, test_list, player, show=False):
    """
    Has the Wordle playing agent play every word in the test list.
    Prints # of successful games, # of failed games, and average # of guesses for successful games.
    """

    print("Now testing player:", player)

    wins = 0
    losses = 0
    total_turns = 0
    total_turns_wins = 0
    worst_perf = 0

    for i in range(len(test_list)):
        soln = test_list[i]

        game = Wordle(guesses_list, soln_list, max_turns=100)

        green_pairs, yellow_pairs, gray_letters = generate_feedback('arise', soln)
        #generate init feedback based on starting guess 'arise'
        game.makeMove('arise', green_pairs, yellow_pairs, gray_letters)
        #similar with play_game_manual(), if you want the player to select its own starting
        #word each time, or are using a different word list, then comment out the above lines.

        while not game.isTerminal:
            if player == "random":
                move = game.greedyRandomSelect()
            elif player == "minimax":
                move = game.minimaxSelect()
            else:
                print("Please choose 'minimax' or 'random' player.")
                exit()

            if move == None:
                print("Solver failed. Word was:", soln)
                break

            green_pairs, yellow_pairs, gray_letters = generate_feedback(move, soln)
            game.makeMove(move, green_pairs, yellow_pairs, gray_letters)

        if game.turn_num-1 <= 6:
            if show:
                print("Game %d: Guessed word \"%s\" in %d turns" % (i, soln, game.turn_num-1))
            wins += 1
            total_turns_wins += (game.turn_num - 1)
        else:
            if show:
                print("Game %d: Failed to guess word \"%s\", took %d turns" % (i, soln, game.turn_num-1))
            losses += 1

        if show == True:
            print("Guesses:", game.past_guesses)
            print()

        if game.turn_num-1 > worst_perf:
            worst_perf = game.turn_num-1
        total_turns += (game.turn_num - 1)

    print("Player agent: ", player)
    print("Played %d games" % len(test_list))
    print("Total wins:", wins)
    print("Total losses:", losses)
    print("Average num turns (wins):", total_turns_wins/wins)
    print("Average num turns (overall):", total_turns/len(test_list))
    print("Worst performance: %d turns" % worst_perf)


def main():
    with open("words_soln.txt", "r") as f:
        soln_list = [line.strip() for line in f.readlines()]
    with open("words_guesses.txt", "r") as f:
        guesses_list = [line.strip() for line in f.readlines()]

    guesses_list = guesses_list + soln_list

    #### TESTING CODE FOR COMPARING AGAINST HUMAN PLAYERS ###
    test_list = ['flack', 'hello', 'duchy', 'quail', 'bless', 'prude', 'latte',
        'entry', 'foamy', 'opera', 'happy', 'hoist', 'flick', 'weigh', 'foist',
        'eclat', 'ghoul', 'minim', 'heist', 'solar', 'could', 'theme', 'dicey',
        'clued', 'aging', 'eater', 'taker', 'would', 'spill', 'slimy']

    ### TESTING CODE FOR TESTING OVER ALL POSSIBLE SOLUTIONS ###
    #test_list = soln_list

    #play_game_manual(guesses_list, soln_list, "minimax")
    play_game_automatic(guesses_list, soln_list, test_list, "minimax", show=True)

if __name__ == "__main__":
    main()
