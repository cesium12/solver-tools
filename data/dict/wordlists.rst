.. _wordlists:

Wordlists
=========

You can work with files in the `data/dict` directory using the
:ref:`wordlist API <wordlist>`. You generally work with them by importing them
as global variables from the module `solvertools.wordlist`. They won't be
loaded until you need them. For example:

    >>> from solvertools.wordlist import ENABLE, WORDNET, COMBINED

The directory contains the following files:

`enable.txt`
------------
ENABLE is a public-domain wordlist that is almost exactly the same as the
TWL98 Scrabble tournament wordlist. The words that they disagree on are shitty
words anyway.
From :mod:`solvertools.wordlist`, you can import this list as `ENABLE`.

`npl_allwords2.txt`
-------------------
This is a file distributed by the National Puzzlers' League, a combination of
all the `word lists`_ they have collected. Unlike a Scrabble wordlist, it
contains proper nouns, multi-word phrases, and crossword clue answers.

.. _`word lists`: http://www.puzzlers.org/dokuwiki/doku.php?id=solving:wordlists:about:start

The list contains phrases with spaces in them, as well as accented characters.
I have converted it from Latin-1 (ew!) to UTF-8.
From :mod:`solvertools.wordlist`, you can import this list as `NPL`.

`google1M.txt` and `google200K.txt`
-----------------------------------
These files contain the most frequent 1 million words in the Google corpus, and
the most frequent 200,000 words, respectively, along with their frequency
counts.

The problem with the most frequent 1 million words is that most of them suck.

From :mod:`solvertools.wordlist`, you can import these lists as `Google1M` and
`Google200K`.

`phonetic.txt`
--------------
A phonetic wordlist adapted from the CMU dictionary. Each word is spelled in
rough IPA, sometimes with multiple pronunciations separated by a vertical bar.

Note: the CMU phonetic dictionary is kind of weird. It has some misspellings,
some weird or dialectal pronunciations, and it omits a number of common words.
We may need to write some code to adapt.

From :mod:`solvertools.wordlist`, you can import this list as `PHONETIC`.

`sages_combined.txt`
--------------------
This is the file that I trained the English `language_model` on. It contains
ENABLE, NPL, PHONETIC, and Google200K, all smashed together, with fake
frequency counts for ENABLE, NPL, and PHONETIC. It may contain more by the time
Hunt happens. All the words are smashed into plain ASCII, and spaces are
ignored.

From :mod:`solvertools.wordlist`, you can import this list as `COMBINED`. A
version that preserves spaces is called `COMBINED_WORDY`.

`wordnet.txt`
-------------
This is a list of all the words in WordNet, including many multiple-word
phrases and scientific terms.

From :mod:`solvertools.wordlist`, you can import this list as `WORDNET`.

`wordnet_defs.txt`
------------------
The information about each word in WordNet can be arranged into a "dictionary
definition" for each word. This list is a mapping from words to their
definitions. (If you only need the words, use `WORDNET` instead, because it
takes up much less memory.) Import this list as `WORDNET_DEFS`.

`musicbrainz_artists.txt`
-------------------------
A list of artists that MusicBrainz knows about. They come with reasonably good
frequency counts: for example, although "FRANK SINATRA" and "REGENERATOR" are
both artist names, the first is 100 times more significant.

Import this list as `MUSICBRAINZ_ARTISTS`.

`musicbrainz_albums.txt` and `musicbrainz_artist_album_rel.txt`
---------------------------------------------------------------
A list of album titles with frequency counts. Import this list as
`MUSICBRAINZ_ALBUMS`.

To associate these albums with the artists who performed them, you can get a
mapping from artist to (album, frequency) under the name
`MUSICBRAINZ_ARTIST_ALBUMS`.

`musicbrainz_tracks.txt` and `musicbrainz_artist_track_rel.txt`
---------------------------------------------------------------
A list of song titles with frequency counts. Import this list as
`MUSICBRAINZ_TRACKS`.

You can also get a mapping from artist to (title, frequency) under the name
`MUSICBRAINZ_ARTIST_TRACKS`.

`imdb_movies.txt`
-----------------
A list of movie titles, mapped to a "relevance" score we computed that is
higher for more well-known movies. Import this list as `IMDB_MOVIES`.

`imdb_actors.txt`
-----------------
A list of movie actors, mapped to a "relevance" score indicating how many and
how prominent roles they have had. Import this list as `IMDB_ACTORS`.

`wikipedia_en_titles.txt`
-------------------------
A large list of Wikipedia article titles, including redirects. Import this list
as `WIKIPEDIA`.

Updating pickle files
---------------------

For efficiency, once these wordlists have been loaded, they are stored as
pickle files in the `data/pickle/` directory. If you change one of these
wordlists for some reason, you will need to remove the corresponding pickle
file so that it gets updated.

*Rob Speer, 2010*
