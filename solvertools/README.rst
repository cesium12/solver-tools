.. _solvertools:

The `solvertools` package
=========================

This is the main `solvertools` package, containing many useful Python tools
that you can use when solving puzzles.

It has the following contents:
    
    :ref:`all.py`
        Imports everything in this documentation (and probably a lot more)
        into the global namespace. It means you can type this at an interactive
        Python prompt and be able to use all the examples in this
        documentation::

            from solvertools.all import *

    :ref:`calendars <calendars>`/
        Calendar tools by Enrico Spinielli, including all major world
        calendars.

    :ref:`cipher <cipher>`/
        Functions for performing and undoing simple ciphers.

    :ref:`model <model>`/
        Back-end NLP code that can figure out what reasonable English text
        looks like.

    :ref:`phonetic <phonetic>`/
        Works with phonetic representations of English words, in all their
        messiness.

    :ref:`puzzlebase <puzzlebase>`/
        An interface to a large database of information about words, which
        can be used to solve crossword clues and find common threads between
        words, among other things.

    :ref:`wiki <wiki>`/
        Tools for automatically reading and writing information on the
        MysteryWiki.

    :ref:`extensions <extensions>`/
        C or C++ code that makes Solvertools run faster.
    
    lib/
        External code that we found useful.

    :ref:`alphabet.py`
        Rob's code for mapping between different sequences of symbols. Might
        be too generalized. Various simple :ref:`ciphers <ciphers>`
        will build on this,
        so that (for example) you can compute a Caesar cipher in Greek as
        easily as in English.

    :ref:`letter_stats.py`
        Does frequency analysis of letters in text, often the first step
        to breaking a cipher.

    :ref:`puzzle_array.py`
        Tools for interpreting regular expressions, and indexing into them
        as if they were non-deterministic strings.

    :ref:`regex.py`
        Tools for interpreting regular expressions, and indexing into them
        as if they were non-deterministic strings.

    :ref:`util.py`
        Generally useful utilities, particularly for file I/O.

    :ref:`wordlist.py`
        Lazily-loaded wordlists that let you quickly determine whether a word
        is valid (for example, in Scrabble or in a crossword).

    `secrets.py`
        You need to store a given Manic Sages password in this file, or else
        you won't be able to use the online parts of Solvertools.

Sub-packages:

.. toctree::
   :maxdepth: 2

   anagram/README
   calendars/README
   cipher/README
   model/README
   phonetic/README
   puzzlebase/README
   wiki/README
   extensions/README

.. _wordlist.py:

`wordlist.py` -- quick wordlist lookups
---------------------------------------
.. automodule:: solvertools.wordlist
   :members:

.. _alphabet.py:

`alphabet.py` -- many different alphabets
-----------------------------------------
.. automodule:: solvertools.alphabet
   :members:

.. _util.py:

`util.py` -- utilities for working with files
---------------------------------------------
.. automodule:: solvertools.util
   :members:

.. _puzzle_array.py:

`puzzle_array.py` -- grids of puzzling information
--------------------------------------------------
.. automodule:: solvertools.puzzle_array
   :members:

.. _regex.py:

`regex.py` -- regular expression hacks
--------------------------------------
.. automodule:: solvertools.regex
   :members:

`letter_stats.py` -- letter frequency analysis
----------------------------------------------
.. automodule:: solvertools.letter_stats
   :members:

.. _all.py:

`all.py` -- import everything at once
-------------------------------------
.. automodule:: solvertools.all
   :members:


