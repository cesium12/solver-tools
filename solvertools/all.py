"""
`solvertools.all` provides a quick way to import a lot of useful functions from
the various parts of Solvertools, which is particularly useful at the command
line:

    >>> from solvertools.all import *

Don't do this in actual modules you want other people to use, because it
puts everything in the same namespace and makes functions impossible to track
down. But in interactive Python, it's fine.

Every function and class described by this documentation will be imported at
the top level, as well as global variables (which can be wordlists such as
`ENABLE` and `COMBINED`).

You can type dir() afterwards to see a huge list of the names that are defined.
In IPython, type a function name followed by two question marks (such as
`split_words??`) to see its documentation.
"""
from solvertools.alphabet import *
from solvertools import calendar
from solvertools.cipher.amino import *
from solvertools.cipher.braille import *
from solvertools.cipher.morse import *
from solvertools.cipher.semaphore import *
from solvertools.cipher.caesar import *
from solvertools.cipher.vigenere import *
from solvertools.model.language_model import *
from solvertools.model.numbers import *
from solvertools.model.tokenize import *
from solvertools.phonetic.arpabet import *
from solvertools.phonetic.roman_ipa import *
from solvertools.puzzle_array import *
from solvertools.puzzlebase.wordplay import *
from solvertools.puzzlebase.mongo import known_word, valid_for_scrabble, get_word, get_relations, get_freq, DB
from solvertools.puzzlebase.clue import *
from solvertools.regex import *
from solvertools.util import *
from solvertools.wiki.puzzlepage import PuzzlePage, editgrid_safe_name, make_puzzle, make_group
from solvertools.wordlist import *

