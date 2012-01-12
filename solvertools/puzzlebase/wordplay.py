from solvertools.puzzlebase.mongo import DB
from solvertools.wordlist import alphanumeric_only, alphagram, word_pattern, letter_bank
from solvertools.anagram.anahash import anahash
import logging
import math

logger = logging.getLogger(__name__)

def log2(x):
    return math.log(x) / math.log(2)

def find_by_alphagram(input):
    "Find words with a given alphagram."
    input = alphagram(input)
    for result in DB.wordplay.find({'alphagram': input}):
        yield result['text'], result['freq']

def find_by_letter_bank(input):
    "Find words with a given letter bank."
    input = letter_bank(input)
    for result in DB.wordplay.find({'letterbank': input}):
        yield result['text'], result['freq']

def find_by_word_pattern(input):
    "Find words with a given word pattern."
    input = word_pattern(input)
    for result in DB.wordplay.find({'wordpattern': input}):
        yield result['text'], result['freq']

def add_wordplay(word, freq):
    """
    Add a word to the wordplay table.
    """
    key = alphanumeric_only(word)
    ahash = anahash(word)
    agram = alphagram(key)
    wordpat = word_pattern(key)
    lbank = letter_bank(key)
    goodness = log2(freq) + len(word)

    logger.info((word, freq))

    return DB.wordplay.update(
        {'text': word},
        {'$set': {'alphagram': agram, 'freq': freq,
                  'wordpattern': wordpat, 'letterbank': lbank,
                  'anahash': ahash, 'goodness': goodness}},
        upsert=True
    )

def _wordplay_from_wordlist(wordlist, multiplier=1):
    """
    Add an entire wordlist to the wordplay table.
    """
    for word in wordlist:
        freq = wordlist[word]
        if not isinstance(freq, (int, long, float)):
            freq = 1
        add_wordplay(word, freq*multiplier)

def _wordplay_from_ngrams(file, cutoff=10000):
    """
    Add an ngrams file to the wordplay table.
    """
    if isinstance(file, basestring):
        file = open(file)
    for line in file:
        words, freq = eval(line.strip())
        if freq >= cutoff:
            phrase = ' '.join(words)
            add_wordplay(phrase, freq)
            logger.info((phrase, freq))

