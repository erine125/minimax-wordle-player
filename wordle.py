########################################
# CS63 Final Project
# Qingyun Catherine Wang
# Spring 2022, Swarthmore College
########################################

import collections
import random

class Wordle:

    def __init__(self, guesses_list, soln_list, turn_num=1, max_turns=6, wordlength=5):
        self.turn_num = turn_num
        self.max_turns = max_turns

        self.guesses_list = guesses_list # list of available guesses/moves
                                        # this should be a superset of the list of solutions.
        self.soln_list = soln_list #list of available solutions

        #store feedback given from each guess as a member variable.
        #store feedback as 3 separate lists: green, yellow, and gray lists.

        self.green_pairs = [] #list of (position, letter) tuples
        self.yellow_pairs = [] #list of (position, letter) tuples
        self.gray_letters = [] #list of letters (position doesn't matter for gray)

        self.past_guesses = [] #list of guesses made
        self.wordlength = wordlength #length of words for the game (default 5)

    def greedyRandomSelect(self):
        """
        A baseline select method to compare Minimax against.
        This method randomly selects its guess from the set of words consistent
        with the clues it's given. In other words, an agent that uses this
        selection method only guesses words that are completely consistent
        with information gained from previous guesses, and chooses randomly
        from those words.

        -------
        returns: guess <string>: selected word to guess
        """
        new_wordlist = filter_wordlist(self.guesses_list, self.green_pairs, self.yellow_pairs, self.gray_letters)
        #since this method is greedy, the guess list itself is filtered each time we gain info.
        self.guesses_list = new_wordlist

        try:
            guess = random.choice(new_wordlist)
        except IndexError:
            print("No word in solution list consistent w/ feedback")
            return None

        return guess

    def minimaxSelect(self):
        """
        Selects guesses using Minimax selection method.
        Models the game as an adversarial game between 2 players: one player
        selecting and an adversary picking the hardest possible solution. Models
        a depth-limit-2 Minimax search for the selecting player.

        Player's goal is to minimize remaining search space after guessing word;
        adversary's goal is to maximize it. Selects the word that minimizes the
        maximum remaining search space over all possible adversary moves.

        i.e. chooses the best word to win the game in the worst case.
        -----
        returns: bestWord <string>: best word to guess next according to Minimax selection.
        """

        self.soln_list = filter_wordlist(self.soln_list, self.green_pairs, self.yellow_pairs, self.gray_letters)
        #filter solution list based on feedback we have - don't want to consider any solutions we know can no longer be the case.
        #however, we DON'T want to filter guesses list - we want to consider guesses that might not be possible,
        #if they might provide us with more info.

        if len(self.soln_list) <= 2: #if only 1 possible solution left, that must be the answer.
                                    #if only 2 left, we have a 50/50 shot, so try guessing one
            try:
                return random.choice(self.soln_list)
            except IndexError:
                print("No word in solution list consistent w/ feedback")
                return None

        bestValue = float('inf') #since we are minimizing this value, start at inf
        bestWord = None

        for guess in self.guesses_list: #selecting player's 'moves'
            max = 0

            for soln in self.soln_list: #adversary player's 'moves'

                #evaluate game state as the size of the search space remaining
                #given both player's 'moves'
                value = eval(guess, soln, self.soln_list)

                if value > max:
                    max = value

                if max > bestValue:
                #if the max of this branch already exceeds our minimum overall value,
                #we know that this move will never be chosen, so we can prune.
                    break

            if max < bestValue:
                bestValue = max
                bestWord = guess

        return bestWord

    def makeMoveManual(self, guess):
        """
        Given a guess chosen by the AI player, prints guess out to terminal.
        Prompts user for feedback, and stores that feedback in member variables.

        User must enter feedback as a 5-digit string:
        0 - gray (letter is not present in the secret word)
        1 - yellow (letter is present, but in the wrong spot)
        2 - green (letter is in the right spot)

        -----
        params: guess <string>: guess chosen by program.

        returns: none, but sets member variables to store feedback.
        """
        print("Guess:", guess)
        print()

        feedback = input("Enter feedback:")

        while not feedback.isnumeric() or len(feedback) !=  5 or feedback.strip('012'):
            print("Feedback must be 5 digits containing only 0, 1, 2")
            feedback = input("Enter feedback:")

        yellow_pairs = []
        green_pairs = []
        gray_letters = []

        for i in range(len(feedback)):
            if int(feedback[i]) == 0:
                gray_letters.append(guess[i])

            if int(feedback[i]) == 1:
                yellow_pairs.append((i, guess[i]))

            if int(feedback[i]) == 2:
                green_pairs.append((i, guess[i]))

        self.yellow_pairs = yellow_pairs
        self.green_pairs = green_pairs
        self.gray_letters = gray_letters

        self.turn_num+=1
        self.past_guesses.append(guess)

    def makeMove(self, guess, green_pairs, yellow_pairs, gray_letters):
        """
        automated version of makeMoveManual that allows feedback to be directly
        passed in from another function rather than entered by a user.
        -----
        params: guess <string>: guess chosen by program.

        returns: none, but sets member variables to store feedback.
        """

        self.yellow_pairs = yellow_pairs
        self.green_pairs = green_pairs
        self.gray_letters = gray_letters

        self.turn_num+=1
        self.past_guesses.append(guess)


    @property
    def isTerminal(self):
        """
        Boolean indicating whether the game has ended.
        Game ends if program guesses word correctly (all 5 letters are green),
        or if the game has reached the max number of turns.
        """
        if len(self.green_pairs) == self.wordlength or self.turn_num > self.max_turns:
            self._terminal = True
        else:
            self._terminal = False
        return self._terminal


################ HELPER FUNCTIONS #####################
def filter_wordlist(wordlist, green_pairs, yellow_pairs, gray_letters):
    """
    Given a list of words and set of information (in the form of green, yellow,
    and gray letters), returns a new list that contains only the words from the
    wordlist that are consistent with said feedback.
    """
    new_guesses_list = []
    for word in wordlist:
        if word_consistent(word, green_pairs, yellow_pairs, gray_letters):
            new_guesses_list.append(word)

    return new_guesses_list

def word_consistent(word, green_pairs, yellow_pairs, gray_letters):
    """
    Given a word and information in the form of green, yellow, and gray letters,
    determines if word is consistent w/ said information (returns True if so)

    Adapted from:
    https://www.kerrigan.dev/2022/01/10/building-a-wordle-solver-in-python.html
    """
    letter_counts = collections.Counter()
    for letter in word:
        letter_counts[letter] += 1

    for (p, l) in green_pairs:
        if word[p] != l:
            # green pair does not match
            return False
        else:
            # green letters "use up" one of the solution letters
            letter_counts[l] -= 1

    # not have letter l at position p for any yellow pair (p, l)
    for (p, l) in yellow_pairs:
        if word[p] == l:
            # letter does match, but it shouldn't
            return False
        else:  # ...and contain letter l somewhere, aside from a green space
            # doesn't contain this letter,
            # or perhaps doesn't contain it enough times
            if letter_counts[l] <= 0:
                return False
            else:
                # yellow letters "use up" one of the solution letters
                letter_counts[l] -= 1

    # contain no gray letters in excess (not "used up")
    for l in gray_letters:
        if letter_counts[l] != 0:
            return False

    return True

def generate_feedback(guess, soln):
    """
    Given a word and solution, generates feedback in the form of green, yellow,
    and gray letters.

    Adapted from:
    https://www.kerrigan.dev/2022/01/10/building-a-wordle-solver-in-python.html
    """
    # sanity check
    assert len(soln) == len(guess)

    # counts all the letters in the solution word
    letter_counts = collections.Counter()
    for letter in soln:
        letter_counts[letter] += 1

    # selects all (position, letter) pairs where the letters in soln and guess are equal
    green_pairs = [(p1, soln_letter) for ((p1, soln_letter), guess_letter)
                   in zip(enumerate(soln), guess) if soln_letter == guess_letter]

    # subtract the green letters from the letter counts,
    # since green letters "use up" letters from the solution word.
    for (_, letter) in green_pairs:
        letter_counts[letter] -= 1

    yellow_pairs = []
    for pos, letter in enumerate(guess):
        # there are excess letters that aren't already marked green
        if letter_counts[letter] > 0 and (pos, letter) not in green_pairs:
            # append this pair
            yellow_pairs.append((pos, letter))
            # subtract one from excess letter count; yellow letters "use up" solution word letters.
            letter_counts[letter] -= 1

    # all remaining pairs are gray
    gray_pairs = [pair for pair in enumerate(guess) if pair not in green_pairs and pair not in yellow_pairs]
    gray_letters = [l for (p,l) in gray_pairs]

    return green_pairs, yellow_pairs, gray_letters

def eval(guess, soln, wordlist):
    """
    Given a guess, hypothetical solution, and solution list, evaluates
    how good a (guess,soln) pair is as a value of the length of the filtered
    wordlist (lower value = better guess, since more of the search space can be
    eliminated through this guess).
    """
    green_pairs, yellow_pairs, gray_letters = generate_feedback(guess, soln)
    filtered_wordlist = filter_wordlist(wordlist, green_pairs, yellow_pairs, gray_letters)
    return len(filtered_wordlist)
