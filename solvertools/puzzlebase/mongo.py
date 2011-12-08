"""
This module provides the basic functions to get data into and out of the
MongoDB database that contains the Puzzlebase.

There are three collections (a.k.a. "tables") in the Puzzlebase:

    - `DB.words`: Lists all known words and phrases, and their frequencies.
    - `DB.relations`: How words are connected to other words.
    - `DB.alphagrams`: Very similar to `DB.words`, but also stores each word
      or phrase as an "alphagram" -- that is, its letters in alphabetical
      order. This can be used by an anagrammer to turn sets of letters into
      relevant words.

There may be another collection called `DB.totals`, which counts the number of
times each word appears in each relation. This is not used directly, but it is
created as an intermediate step of building the "interestingness" scores, as
rare relations are more interesting than common ones. The code to compute
`DB.totals` appears in `mapreduce.js`.

Most of the operations work with the `DB.relations` collection. Each entry
in DB.relations should have the following fields:

    - `words`: a list of all words involved in the relation. (You can search
      for relations by matching any of the words they contain.)
    - `value`: if the relation represents an operation that yields a result
      (such as concatenating "DOUBLE" and "SPEAK" to give "DOUBLESPEAK"),
      then the result is stored and indexed in `value`.
    - `freq`: the number of times this was observed, in some sense.
    - `interestingness`: When a relation holds between two (or more) words with
      a higher frequency than one would expect from similar relations, it is
      deemed *interesting*. Relations that are very common (such as "you can add
      S to this word") are not very interesting. Search results are sorted by
      interestingness.

In actuality, some of the less-frequent relations are missing "interestingness" scores because they were taking too long to calculate. These will show up
at the end of the list.

The words in `DB.relations` are all stored in the normalized form that results
from the :func:`alphanumeric_only` function. Keep in mind that this removes
spaces.

Once this module is imported, you have a connection to the MongoDB stored in
the global variable `DB`.
"""

from pymongo import Connection, ASCENDING, DESCENDING
from solvertools.wordlist import alphanumeric_only, alphagram
from solvertools.config import DB_USERNAME, DB_PASSWORD
import math

CONNECTION = Connection('tortoise.csc.media.mit.edu')
DB = CONNECTION.puzzlebase
import logging
logger = logging.getLogger(__name__)
DB.authenticate(DB_USERNAME, DB_PASSWORD)

#DB.words.ensure_index('key')
DB.relations.ensure_index([('words', ASCENDING),
                           ('interestingness', DESCENDING),
                           ('freq', DESCENDING)])

DB.relations.ensure_index([('words', ASCENDING),
                           ('value', ASCENDING),
                           ('interestingness', DESCENDING),
                           ('freq', DESCENDING)])
DB.relations.ensure_index([('words', ASCENDING),
                           ('rel', ASCENDING),
                           ('freq', DESCENDING)])

DB.alphagrams.ensure_index([('alphagram', ASCENDING),
                            ('goodness', DESCENDING)])
DB.alphagrams.ensure_index([('anahash', ASCENDING), ('goodness', DESCENDING)])

def add_relation(rel, words, value=None, freq=1):
    """
    Add the fact that the relation `rel` holds between `words` to the database.
    If this is already known, update its frequency.
    """
    # do an upsert on rel, [word1, word2], setting the freq
    words = [alphanumeric_only(word) for word in words]
    return DB.relations.update(
        {'rel': rel, 'words': words, 'value': value},
        {'$set': {'freq': freq}},
        upsert=True
    )

def add_word(fulltext, freq):
    """
    Store the word or phrase represented by `fulltext` in the database,
    along with its frequency.
    """
    key = alphanumeric_only(fulltext)
    return DB.words.update(
        {'_id': key},
        {'$set': {'text': fulltext},
         '$inc': {'freq': freq}},
        upsert=True
    )

def get_word(text):
    """
    Get the DB.words entry for `text`, or None if it does not exist.
    """
    key = alphanumeric_only(text)
    return DB.words.find_one({'_id': key})

def get_relations(text):
    """
    Get an iterator of all relations that `text` appears in.
    """
    key = alphanumeric_only(text)
    return DB.relations.find({'words': key})

def get_anagrams(text):
    """
    Get all the known words that anagram to `text`.
    """
    key = alphagram(alphanumeric_only(text))
    found = set([alphanumeric_only(text)])
    anagrams = []
    for rec in DB.alphagrams.find({'alphagram': key}):
        text = rec['text']
        textkey = alphanumeric_only(text)
        if textkey not in found:
            anagrams.append((rec['text'], rec['freq']))
            found.add(textkey)
    return anagrams

def get_freq(text):
    """
    Get the frequency of `text`, or 0 if it is not in the DB.words collection.
    """
    key = alphanumeric_only(text)
    found = DB.words.find_one({'_id': key})
    if not found:
        return 0
    else:
        return found['freq']

def add_from_wordlist(wordlist, multiplier=1, lexical=True, max=None):
    """
    Add all the words from a given wordlist.
    """
    for word in wordlist:
        freq = wordlist[word]
        if max is not None and freq >= max:
            continue
        if not isinstance(freq, (int, long, float)):
            freq = 1
        add_word(word, freq*multiplier)
        add_relation('in_wordlist', [word], wordlist.filename, freq*multiplier)
        logger.info((wordlist.filename, word, freq*multiplier))

def known_word(word):
    # deprecated
    return DB.relations.find_one(
        {'rel': 'in_wordlist', 'words': alphanumeric_only(word)}
    )

def valid_for_scrabble(word):
    """
    This function uses the database to establish whether a word is a valid
    Scrabble word (appearing in ENABLE, which is nearly the same as OSPD3).
    """
    return DB.relations.find_one(
        {'rel': 'in_wordlist',
         'words': word,
         'value': 'enable'
        }
    )

def make_alphagrams(wordlist):
    for word, freq in wordlist.iteritems():
        add_alphagram(word, freq)

