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
import json
import os
import requests

class Hangman:

    def __init__(self, lifepoints):
        self.lives = int(lifepoints)
        self._word = self.get_Word()
        self.display = ['_' for char in self._word]
        self._state = True # Flag variable
        self.answered = [] # Answered letters
        self.hintcounter = 0 # Hints used
        self.hintdisplay = f' (2) hint: -3 lives ({self.hintcounter}/3)'
        self._definition = '' 
        self.game()

    def get_Word(self):
        """
        Function that generates a random word of the list "words"
        """
        response = requests.get('https://random-word-api.herokuapp.com/word')
        word = str(response.content[2:-2])[2:-1]
        return word
    
    def guessChar(self, guess):
        """
        Receives a letter and checks if it is in the word.
        If it is, shows the letter in the word.
        If not, decreases lives.
        """
        if guess == str(1): # Player used definition
            if self.lives <= 5:
                print('You can\'t do that. You need more lives')
            else:
                self.lives -= 5
                response = requests.get('https://api.dictionaryapi.dev/api/v2/entries/en/' + self._word)
                if 205 <= len(response.content) <= 208: # length of no definition is around these numbers
                    self._definition = 'There is no definition in our dictionary, sorry. We haven\'t taken any lives'
                    self.lives += 5
                else:
                    try:
                        dic = json.loads(str(response.content)[3:-2])
                        definition = dic['meanings'][0]['definitions'][0]['definition'] # Only takes the first possible meaning
                        self._definition = definition
                    except:
                        print('There is an error, definition disallowed this game.')
                        self._definition = 'Error, there is no definition in our API'
        elif guess == str(2): # Player used hint
            if self.lives <= 3:
                print('You can\'t do that. You need more lives')
            else:
                self.lives -= 3
                i = 0
                while i < len(self.display):
                    if self.display[i] == '_':
                        self.display[i] = self._word[i]
                        i += len(self.display)
                        self.hintcounter += 1
                        self.hintdisplay = f' (2) hint: -3 lives ({self.hintcounter}/3)'
                        if self.hintcounter > 2:
                            self.answered.append(str(2))
                            self.hintdisplay = ' No more hints allowed '
                    if ''.join(self.answered) == self._word:
                        self.winGame()
                    i += 1
        elif guess not in self._word:
            self.answered.append(guess)
            self.lives -= 1
            if self.lives == 0:
                self.finishGame()
        else:
            self.answered.append(guess)
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
        if os.name == 'nt':
            os.system('cls')
        else: 
            os.system('clear')
        
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
        try:
            f = open(history, 'r')
            record = json.load(f)
            f.close()
            record['wins'] += 1
            print('Current stats:')
            print(record)
            f = open(history, 'w')
            f.write(json.dumps(record))
            f.close()
        except FileNotFoundError:
            record = {'wins': 1, 'losses': 0}
            fichero = open(history, 'w')
            fichero.write(json.dumps(record))
            fichero.close()

    def finishGame(self):
        """
        The player has no more lives, he has lost the game
        """
        print('Sorry! You lost all your lives and lost the game.')
        print(f'The word was: {self._word}')
        self._state = False
        try:
            f = open(history)
            record = json.load(f)
            f.close()
            record['losses'] += 1
            print('Current stats:')
            print(record)
            f = open(history, 'w')
            f.write(json.dumps(record))
            f.close()
        except FileNotFoundError:
            record = {'wins': 0, 'losses': 1}
            fichero = open(history, 'w')
            fichero.write(json.dumps(record))
            fichero.close()

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
            print('\n --- Handouts --- ')
            if self._definition != '':
                print(f' definition: {self._definition}')
                print(self.hintdisplay)
            else:
                print(' (1) definition: -5 lives ')
                print(self.hintdisplay)
            guess = input('\nGuess a letter or a word: ')
            self.makeGuess(guess)
        time.sleep(3)


# Words are stored in a web, we get the word with requests module
history = 'WinRecord.json'
lifepoints = 0
while int(lifepoints) <= 0:
    try:
        lifepoints = int(input('How many lives do you want to have? (recommended: 10) \n'))
    except:
        print('Error. You have to write a number.')
a = Hangman(lifepoints)