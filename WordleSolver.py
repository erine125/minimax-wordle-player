from wordle import Wordle, filter_wordlist, word_consistent, generate_feedback
from testGame import play_game_manual

def main():
    print("Welcome to Wordle Solver. This solver uses the rule set and word lists from the online Wordle game.\n")

    choice = input("Choose player: minimax or random (enter 'm' or 'r'): ")
    while choice != 'm' and choice != 'r':
        choice = input("enter 'm' or 'r': ")
    if choice == 'm':
        agent = 'minimax'
    if choice == 'r':
        agent = 'random'


    print("Enter feedback as 5 digits:")
    print("0 - gray")
    print("1 - yellow")
    print("2 - green")

    with open("words_soln.txt", "r") as f:
        soln_list = [line.strip() for line in f.readlines()]
    with open("words_guesses.txt", "r") as f:
        guesses_list = [line.strip() for line in f.readlines()]

    guesses_list = guesses_list + soln_list

    print("\nRunning %s agent..." % agent)
    play_game_manual(guesses_list, soln_list, agent)

main()
