.. _wordlists:

Wordlists
=========

You can work with files in the `data/dict` directory using the
:ref:`wordlist API <wordlist>`.

The directory contains the following files:

`enable.txt`
------------
ENABLE is a public-domain wordlist that is almost exactly the same as the
TWL98 Scrabble tournament wordlist. The words that they disagree on are shitty
words anyway. You can access this list as `solvertools.wordlist.ENABLE`.

`npl_allwords2.txt`
-------------------
This is a file distributed by the National Puzzlers' League, a combination of
all the wordlists_ they have collected. Unlike a Scrabble wordlist, it contains
proper nouns, multi-word phrases, and crossword clue answers.

The list contains phrases with spaces in them, as well as accented characters.
I have converted it from Latin-1 (ew!) to UTF-8. You can access this list as
`solvertools.wordlists.NPL`.

_wordlists: http://www.puzzlers.org/dokuwiki/doku.php?id=solving:wordlists:about:start

`google1M.txt` and `google200K.txt`
-----------------------------------
These files contain the most frequent 1 million words in the Google corpus, and
the most frequent 200,000 words, respectively, along with their frequency
counts.

The problem with the most frequent 1 million words is that most of them suck.

You can access these lists as `solvertools.wordlist.Google1M` and
`solvertools.wordlist.Google200K`.

`phonetic.txt`
--------------
A phonetic wordlist adapted from the CMU dictionary. Each word is spelled in
rough IPA, sometimes with multiple pronunciations separated by a vertical bar.

Note: the CMU phonetic dictionary is kind of weird. It has some misspellings,
some weird or dialectal pronunciations, and it omits a number of common words.
We may need to write some code to adapt.

You can access this list as `solvertools.wordlist.PHONETIC`.

`sages_combined.txt`
--------------------
This is the file that I trained the English `language_model` on. It contains
ENABLE, NPL, PHONETIC, and Google200K, all smashed together, with fake
frequency counts for ENABLE, NPL, and PHONETIC. It does not include any of the
phrases with spaces from NPL, and all the text is smashed down into plain
ASCII.

You can access this list as `solvertools.wordlist.COMBINED`.

Updating pickle files
---------------------

For efficiency, once these wordlists have been loaded, they are stored as
pickle files in the `data/pickle/` directory. If you change one of these
wordlists for some reason, you will need to remove the corresponding pickle
file so that it gets updated.

*Rob Speer, 2010*
