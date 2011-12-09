from solvertools.puzzlebase.mongo import DB
from solvertools.wordlist import alphanumeric_only, alphagram
from solvertools.anagram.anahash import anahash
import logging
import math

logger = logging.getLogger(__name__)

def log2(x):
    return math.log(x) / math.log(2)

def add_alphagram(word, freq):
    """
    Add a word to the alphagram table.
    """
    key = alphanumeric_only(word)
    ahash = anahash(word)
    goodness = log2(freq) + len(word)
    logger.info((word, freq, ahash))

    return DB.alphagrams.update(
        {'alphagram': alphagram(key),
         'text': word},
        {'$set': {'freq': freq, 'anahash': ahash, 'goodness': goodness}},
        upsert=True
    )

def alphagrams_from_wordlist(wordlist, multiplier=1):
    for word in wordlist:
        freq = wordlist[word]
        if not isinstance(freq, (int, long, float)):
            freq = 1
        add_alphagram(word, freq*multiplier)

def alphagrams_from_ngrams(file, cutoff=10000):
    if isinstance(file, basestring):
        file = open(file)
    for line in file:
        words, freq = eval(line.strip())
        if freq >= cutoff:
            phrase = ' '.join(words)
            add_alphagram(phrase, freq)
            logger.info((phrase, freq))


