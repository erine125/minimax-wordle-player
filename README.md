### Overview

This project implements a Wordle solver agent using Minimax.

### Files (& running instructions)

- `wordle.py`: Contains the class definition for the `Wordle` class, as well as helper functions.
- `testGame.py`: Contains 2 functions for playing the game manually or automatically: `play_game_manual()` and `play_game_automatic()`. The `play_game_automatic()` function can be used to test the performance of the Minimax and greedy random players. The function takes in a list of words to test (`test_list`) and a player type (`'minimax'` or `'random'`) and will run the game over the entire test list, printing out a report of its performance, including wins, losses, average guesses, and worst case performance.
To test this code, modify `test_list` to the list of words you want to test, and set the player type to `'minimax'` or `'random'`. The `show` flag instructs the program to print out all the guesses the agent made in each game. By default it is set to `False`, so the program will only print out the overall results (wins, losses, average, and worst). Set the flag to `True` to print out the actual guesses.
  The program currently uses the actual Wordle wordlists as the list of possible guesses and solutions; however, if you want to test it on different word lists, simply replace the file names in `main()`.
  The program currently hard codes in the starting word `'arise'` to save computation time. However, if you are using a different word list, or want the program to compute its own starting word, simply comment out the lines containing `'arise'` (11-13, 61-63).

- `WordleSolver.py`: A user interface for using the AI agent to play Wordle. This function calls the `play_game_manual()` function on the set of actual words used in the Wordle game.
  User will be prompted to choose between the Minimax and greedy random players by entering `'m'` or `'r'` respectively. The program will output a guess, and the user gives program feedback in the form of 5-digit strings. Each digit represents a letter in the agent's guess, and each number represents a different type of Wordle clue square:
  
  0 - gray letter (letter is not in the secret word)
  
  1 - yellow letter (letter is in the word, but in the wrong place)
  
  2 - green letter (letter is in the right place)
  

  For example: if the program guesses `'among'`, and the secret word is `'axiom'`, the user should enter: `21100`
  Note that, like in the real Wordle game, duplicate letters should be marked as gray if they appear in excess of the number of times they actually appear. For example: if the program guesses `'canal'`, and the secret word is `'cater'`, the user should enter: `22000`. This is how the real Wordle game gives feedback, so a user can use the program to help them play a game of Wordle by entering the feedback from their Wordle game and having the program suggest the best guesses.

The repository also contains 2 files containing word lists:

- `words_soln.txt`: All possible solutions to the game.
- `words_guesses.txt`: All words that are allowed as guesses but are not possible solutions to the game.

These word lists were taken from the original Wordle game by Josh Wardle.
