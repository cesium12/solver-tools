The `solvertools` package
=========================

This is the main `solvertools` package, containing many useful Python tools
that you can use when solving puzzles.

It has the following contents:
    
    :ref:`google`/
        Python interfaces to useful Google services, such as the Google
        Translate API.

    lib/
        External code that we found useful.

    :ref:`model`/
        Back-end NLP code that can figure out what reasonable English text
        looks like.

    scripts/
        This is not a Python package; it's a collection of useful scripts.

    alphabet.py
        Rob's code for mapping between different sequences of symbols. Might
        be too generalized. Ideally various simple ciphers will build on this,
        so that (for example) you can compute a Caesar cipher in Greek as
        easily as in English.

    :ref:`wordlist.py <wordlist>`
        Lazily-loaded wordlists that let you quickly determine whether a word
        is valid (for example, in Scrabble or in a crossword).

    util.py
        Generally useful utilities, particularly for file I/O.

.. _wordlist:

The `solvertools.wordlist` API
------------------------------
.. automodule:: solvertools.wordlist
    :members:


