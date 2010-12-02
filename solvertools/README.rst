.. _solvertools:

The `solvertools` package
=========================

This is the main `solvertools` package, containing many useful Python tools
that you can use when solving puzzles.

It has the following contents:
    
    :ref:`google <google>`/
        Python interfaces to useful Google services, such as the Google
        Translate API.

    lib/
        External code that we found useful.

    :ref:`model <model>`/
        Back-end NLP code that can figure out what reasonable English text
        looks like.

    :ref:`wordlist.py`
        Lazily-loaded wordlists that let you quickly determine whether a word
        is valid (for example, in Scrabble or in a crossword).

    :ref:`alphabet.py`
        Rob's code for mapping between different sequences of symbols. Might
        be too generalized. Various simple :ref:`ciphers <ciphers>`
        will build on this,
        so that (for example) you can compute a Caesar cipher in Greek as
        easily as in English.

    :ref:`util.py`
        Generally useful utilities, particularly for file I/O.

    :ref:`puzzle_array.py`
        Tools for interpreting regular expressions, and indexing into them
        as if they were non-deterministic strings.

    :ref:`regex.py`
        Tools for interpreting regular expressions, and indexing into them
        as if they were non-deterministic strings.

Sub-packages:

.. toctree::
   :maxdepth: 2

   cipher/README
   google/README
   model/README
   phonetic/README
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

