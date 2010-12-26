from pymongo import Connection, ASCENDING, DESCENDING
from solvertools.wordlist import alphanumeric_only
from solvertools.config import DB_USERNAME, DB_PASSWORD
CONNECTION = Connection('tortoise.csc.media.mit.edu')
DB = CONNECTION.puzzlebase
import logging
logger = logging.getLogger(__name__)
DB.authenticate(DB_USERNAME, DB_PASSWORD)

DB.words.ensure_index('key')
DB.relations.ensure_index([('words', ASCENDING),
                           ('interestingness', DESCENDING),
                           ('freq', DESCENDING)])

DB.relations.ensure_index([('words', ASCENDING),
                           ('value', ASCENDING),
                           ('interestingness', DESCENDING),
                           ('freq', DESCENDING)])


def add_relation(rel, words, value=None, freq=1):
    # do an upsert on rel, [word1, word2], setting the freq
    words = [alphanumeric_only(word) for word in words]
    return DB.relations.update(
        {'rel': rel, 'words': words, 'value': value},
        {'$inc': {'freq': freq}},
        upsert=True
    )

def add_word(fulltext, freq):
    key = alphanumeric_only(fulltext)
    return DB.words.update(
        {'key': key},
        {'$set': {'text': fulltext},
         '$inc': {'freq': freq}},
        upsert=True
    )

def add_from_wordlist(wordlist, multiplier=1, lexical=True):
    for word in wordlist:
        freq = wordlist[word]
        if not isinstance(freq, (int, long, float)):
            freq = 1
        add_word(word, freq)
        add_relation('in_wordlist', [word], wordlist.filename, freq*multiplier)
        if lexical:
            add_relation('lexical', [word], freq=freq*multiplier)
        logger.info((wordlist.filename, word, freq*multiplier))

def known_word(word):
    return DB.relations.find_one(
        {'rel': 'in_wordlist', 'words': word}
    )

def valid_for_scrabble(word):
    return DB.relations.find_one(
        {'rel': 'in_wordlist',
         'words': word,
         'value': 'enable'
        }
    )


