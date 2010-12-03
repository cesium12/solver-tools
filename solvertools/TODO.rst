The TODO list
=============

Things to be done
-----------------
(from David's e-mail in Jan 2010)

- substrings of words that you can remove to make other words
- scrabble operations and then some.
- morse code, braille, semaphore, 
- now that we can index everything into everything, make a bot that watches it
  and says OMG GUYS THIS IS THE ANSWER
  (but only when it's really good)
- interfaces to: imdb, wordnet, decrypto, tineye, etc...
- lists of things
- rhyming word list
- function: known word to phonetic value
- letter frequency tests: pairs, vowel appearance, each pair of words have one letter in common, word lengths, phoneme frequency counts.
- pattern noticer
- stuff to avoid manual typing and formatting (table to puzzle grid, edit grid to list of lists...)
- data visualization
- coloring data in various ways
- highlight certain letters
- framework for writing solvers for logic puzzles
- human hooks (ask human for input)
- conversely, a suggestion system
- boundary detection on images
- look for things that associate numbers with text
- statistical detection of normal english vs. weird

Things that need further explanation
------------------------------------
- boggle bigrammer
- finding a wordlist within a body of text
- indexing into 2d array by string

Things that are done or essentially done now
--------------------------------------------
- simultaneous sorting and indexing
- word grid class (solvertools.puzzle_array)
- diagonalizing (solvertools.puzzle_array)
- indexing functions should have options: spaces count or not, etc.
- LetterNumber class (alphabet.py implements this idea)
- indexing by letters (alphabet.py)
- word lists (with frequency)
- library for dealing with wordlists
- language recognizer (solvertools.google.language)
- transliteration and translation (solvertools.google.language)
- handles unicode okay (utf-8).
- deaccenting characters (at the wordlist library level)
- Caesar Shift operations (solvertools.cipher.caesar)
- importing files in general (PuzzleArray.load_csv)
