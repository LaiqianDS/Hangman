"""
Miniproject Hangman.
This project consists on the classical Hangman game, in which
the player has to guess a word given its length.

The player can guess a letter or the complete word, each
incorrect guess (the letter is not in the word or the word
is wrong), a new part of the hangman will be drawn.

The objective is to guess the entire word before the hangman is 
completely drawn. 

To make it simpler, we have set a number of lives instead of drawing
"""

# Library needed
import random
import time

class Hangman:

    def __init__(self, lifepoints):
        self.lives = lifepoints
        self._word = self.get_Word()
        self.display = ['_' for char in self._word]
        self._state = True # Flag variable
        self.answered = []
        self.game()

    def get_Word(self):
        """
        Function that generates a random word of the list "words"
        """
        return words[random.randint(0,len(words))]
    
    def guessChar(self, guess):
        """
        Receives a letter and checks if it is in the word.
        If it is, shows the letter in the word.
        If not, decreases lives.
        """
        self.answered.append(guess)
        if guess not in self._word:
                self.lives -= 1
                if self.lives == 0:
                    self.finishGame()
        else:
            for i in range(len(self._word)):
                if self._word[i] == guess:
                    self.display[i] = guess

    def guessWord(self, word):
        """
        Receives a word, if the word has the same length of the hidden,
        checks if it is the same. 
        If it is the same word, player wins.
        If not, decreases lives
        """
        if word != self._word:
            self.lives -= 1
            if self.lives == 0:
                return self.finishGame()
        else:
            self.winGame()

    def makeGuess(self, guess):
        """
        Receives the user's guess and checks
        """
        if len(guess) == 1:
            if guess in self.answered:
                print('Letter already given, try another one')
            else:
                self.guessChar(guess)
        
        elif len(guess) == len(self._word):
            self.guessWord(guess)
        
        else:
            print('Lenght error, try again with one letter or a word')

    def winGame(self):
        """
        The player has guessed the hidden word, he/she has won
        """
        print('Congratulations, you\'ve won!')
        print(f'The word was: {self._word}')
        self._state = False

    def finishGame(self):
        """
        The player has no more lives, he has lost the game
        """
        print('Sorry! You lost all your lives and lost the game.')
        print(f'The word was: {self._word}')
        self._state = False

    def __repr__(self):
        """
        Displays the letters guessed correctly
        """
        return ('\n' + " ".join(self.display) + 
                '\n' + 'You still have ' + str(self.lives) + ' lives'+
                '\n' + 'Guessed letters: ' + ", ".join(self.answered))
    
    def game(self):
        while self._state == True:
            print(self)
            guess = input('\nGuess a letter or a word: ')
            self.makeGuess(guess)
        time.sleep(5)

# Words are stored in an text file named 'CommonWords.txt'
words_file = 'CommonWords.txt'
lifepoints = 10

with open(words_file, 'r') as f:
    words = f.read().split() 
    
a = Hangman(lifepoints)