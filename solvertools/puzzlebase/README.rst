.. _puzzlebase:

Puzzlebase: stores craploads of information about words
=======================================================
The Puzzlebase is a MongoDB database running on an external server. It stores
lots of relationships between words that are indexed every which-way,
including:

- `clued_by`: one word appears in a crossword clue, or dictionary definition,
  for another word
- `bigram`: these words together form a common phrase (later applied
  as a bit of a misnomer to trigrams as well)
- `can_adjoin`: these words can be concatenated into a larger word

These relations store the list of words they involve, a possible "value" that
indicates the result of the operation (such as the complete phrase that the
words form), and a frequency indicating how many times this relationship was
observed.

Most relations also store an "interestingness" score that accounts for how high
you would expect the frequency to be. For example, the fact that many words can
adjoin the letter "S" has high frequency, but low interestingness.

.. _clue.py:

`clue.py` -- solves crossword-like clues
----------------------------------------
.. automodule:: solvertools.puzzlebase.clue
   :members:

.. _mongo.py:

`mongo.py` -- retrieves Puzzlebase information from MongoDB
-----------------------------------------------------------
.. automodule:: solvertools.puzzlebase.mongo
   :members:

.. _build.py:

`build.py` -- builds the Puzzlebase
-----------------------------------
This module has all the pieces in it to build the Puzzlebase out of other
sources of information, some of which is included in Solvertools.

It takes on the order of weeks to do it, so there wasn't time to go back and do
it right.

*Rob Speer, 2011*
