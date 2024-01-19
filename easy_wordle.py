#By Max Locketz, CSCI 1913
import display_utility
import random
from wordle import check_word
from words import words

def filter_word_list(words, clues):
  """Given a list of 'words' to check, and a list of tuples or 'clues', each clue representing a time the player has guessed and each tuple containing the word guessed and a string of colors representing the output, checks the list 'words' for words that returns all the same clues as the secret word does. These words are added to 'new_words' and returned."""
  new_words = []
  for word in words:
    count = 0
    for i in range (0, len(clues)):
      for j in range(0, 5):
        if check_word(word.upper(), clues[i][0])[j] == clues[i][1][j]:
          count += 1
          #adds 1 to count for every color string a given word outputs that matches 'clues'
        else:
          continue
    if count >= (5*len(clues)):
      new_words.append(word)
  return new_words
  
def easy_game(secret):
  """Given a 5 letter secret word, plays the easy version of Wordle. After each guess, tells the player how many words are possible, and gives them 5 words to chose from"""
  green_count = 0
  clues = []
  guess = ""
  game = True
  guess_count = 0
  while game:
    isValid = False
    while not isValid:
      guess = input("> ").upper()
      if (guess.lower() in words) and (len(guess) == 5):
        isValid = True
        guess_count += 1
      else:
        print("Not a word. Try again")
    clues.append((guess, check_word(secret, guess)),)
    new_words = filter_word_list(words, clues)
    random.shuffle(new_words)
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
      green_count = 0
    print(f"{len(new_words)} words possible:")
    possible_word_num = 5
    if (len(new_words) < 5):
      possible_word_num = len(new_words)
    for j in range(0, possible_word_num):
      print(new_words[j].lower())
    if (guess_count >= 6):
      game = False
  print(f"Answer: {secret}")

if __name__ == " __main__ " :
  secret = random.choice(words).upper()
  easy_game(secret)