#By Max Locketz, CSCI 1913
import display_utility
import random
from words import words

def check_word(secret, guess):
  """Compares the word guessed to the secret word and returns a list of colors that correspond to each letter of the guess. A Green letter is a letter in the correct spot. A yellow letter is a letter that is in the secret word, but not in the correct spot. A Grey letter is not in the secret word."""
  colors = ["grey"] * 5
  green_letters = []
  yellow_letters = []
  secret_list = list(secret)
  guess_list = list(guess)
  for i in range(0, 5):
    if guess_list[i] == secret_list[i]:
      colors[i] = "green"
      green_letters.append(guess_list[i])
    else:
      for j in range(0, 5):
        if colors[j] == "green":
          continue
        count_left_in_secret = secret_list.count(guess_list[j])
        count_left_in_secret -= green_letters.count(guess_list[j]) 
        count_left_in_secret -= yellow_letters.count(guess_list[j])
        if (guess_list[j] == secret_list[i]) and (count_left_in_secret > 0):
          colors[j] = "yellow"
          yellow_letters.append(guess_list[j])
          #only makes letters yellow if they are in the secret word AND there are some of that letter left in the word.
          #this ensures it doesn't make too many letters yellow
  return colors

def known_word(clues):
  """Given a list of tuples, each tuple representing a time the player has guessed and each tuple containing the word guessed and a string of colors representing the output, returns a string of the known letters in the word, with unkown letters as underscores"""
  known = ""
  known_list = ["_", "_", "_", "_", "_"]
  for i in range(0, len(clues)):
    for j in range(0, 5):
      if clues[i][1][j] == "green":
        known_list[j] = clues[i][0][j]
  for letter in known_list:
    known += letter
  return known
  
def no_letters(clues):
  """Given 'clues', a list of tuples, each tuple representing a time the player has guessed and each tuple containing the word guessed and a string of colors representing the output, returns a string containing all letters the player has guessed that are NOT in the secret word"""
  grey_letters = ""
  grey_letters_set = set()
  green_letters_set = set()
  yellow_letters_set = set()
  for i in range(0, len(clues)):
    for j in range(0, 5):
      if (clues[i][1][j] == "grey"):
        grey_letters_set.add(clues[i][0][j])
        #adds the letters to a set to later remove duplicates
      elif (clues[i][1][j] == "green"):
        green_letters_set.add(clues[i][0][j])
      elif (clues[i][1][j] == "yellow"):
        yellow_letters_set.add(clues[i][0][j])
  grey_letters_list = sorted(grey_letters_set)
  for grey_letter in grey_letters_list:
    if grey_letter in (green_letters_set or yellow_letters_set):
      continue
      #checks to make sure no letters are added to 'no_letters' that are green or yellow in a different guess or position
      #this fixes an issue with a player guessing 2 letters, with one green or yellow, and the other being grey,
      #and it still being added to the grey_letters list
    else:
      grey_letters += str(grey_letter)
  return grey_letters
  
def yes_letters(clues):
  """Given a list of tuples, each tuple representing a time the player has guessed and each tuple containing the word guessed and a string of colors representing the output, returns a string containing all letters the player has guessed that ARE in the secret word"""
  green_yellow_letters = ""
  green_yellow_letters_set = set()
  for i in range(0, len(clues)):
    for j in range(0, 5):
      if (clues[i][1][j] == "green" or clues[i][1][j] == "yellow"):
        green_yellow_letters_set.add(clues[i][0][j])
  green_yellow_letters_list = sorted(green_yellow_letters_set)
  for i in range (0, len(green_yellow_letters_list)):
    green_yellow_letters += str(green_yellow_letters_list[i])
  return green_yellow_letters
  
def game(secret):
  """Given a 5 letter secret word, runs the game Wordle"""
  clues = []
  guess = ""
  game = True
  guess_count = 0
  green_count = 0
  while game:
    isValid = False
    print(f"Known:  {known_word(clues)}")
    print(f"Green/Yellow Letters: {yes_letters(clues)}")
    print(f"Grey Letters: {no_letters(clues)}")
    while not isValid:
      guess = input("> ").upper()
      if (guess.lower() in words) and (len(guess) == 5):
        isValid = True
        guess_count += 1
      else:
        print("Not a word. Try again")
    clues.append((guess, check_word(secret, guess)),)
    for clue in clues:
      for j in range(0, 5):
        if (clue[1][j] ==  "green"):
          display_utility.green(clue[0][j])
          green_count += 1
        elif (clue[1][j] ==  "yellow"):
          display_utility.yellow(clue[0][j])
        elif (clue[1][j] ==  "grey"):
          display_utility.grey(clue[0][j])
      print()
      if green_count >= 5:
        game = False
        #if any given guess has 5 green letters, stops the game
      green_count = 0
    if (guess_count >= 6):
      game = False
      #if the player has guessed 6 times, stops the game
  print(f"Answer: {secret}")

if __name__ == " __main__ " :
  secret = random.choice(words).upper()
  game(secret)