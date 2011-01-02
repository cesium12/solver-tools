from solvertools.puzzlebase.mongo import add_from_wordlist, add_relation
from solvertools.wordlist import NPL, ENABLE, WORDNET, PHONETIC, COMBINED_WORDY, CROSSWORD, PHRASES, WIKIPEDIA
from solvertools.wordnet import morphy_roots
from solvertools.model.tokenize import get_words
import logging
logger = logging.getLogger(__name__)

# oversimplified rule of thumb: any word that appears 1.3 billion times or more
# on Google is a stopword
STOPWORD_CUTOFF = 1300000000

def initial_setup():
    add_from_wordlist(WORDNET, multiplier=10000)
    add_from_wordlist(ENABLE, multiplier=2000)
    add_from_wordlist(NPL, multiplier=5000, lexical=False)
    add_from_wordlist(PHONETIC, multiplier=10000)
    add_from_wordlist(CROSSWORD, multiplier=100, lexical=False)
    add_from_wordlist(WIKIPEDIA, multiplier=5000)
    add_from_wordlist(PHRASES, lexical=False)

def add_roots(wordlist):
    for word in wordlist:
        for lemma in morphy_roots(word):
            add_relation('has_root', [word, lemma])
            logger.info(('has_root', [word, lemma]))

def add_concatenations(wordlist):
    # get the basic logic from n-c
    for word in wordlist:
        freq = wordlist[word]
        for prefixlen in xrange(1, len(word)):
            prefix = word[:prefixlen]
            if prefix in wordlist or len(prefix) == 1:
                suffix = word[prefixlen:]
                if suffix in wordlist or len(suffix) == 1:
                    add_relation('can_adjoin', [prefix, suffix],
                                 word, freq)
                    logger.info(('can_adjoin', [prefix, suffix],
                                word, freq))

def add_clues(mapping):
    """
    Take a word mapping, like CROSSWORD or WORDNET_DEFS. Extract all words from
    the definitions/clues, and give them the symmetric 'has_clue' relation with
    the keyword.
    """
    for word in mapping:
        for clue in mapping[word]:
            add_relation('crossword_clue', [word], clue)
            clue_words = get_words(clue)
            for clue_word in clue_words:
                possibilities = [clue_word] + list(morphy_roots(clue_word))
                for word2 in possibilities:
                    add_relation('clued_by', [word, word2])
                    logger.info(('clued_by', [word, word2]))

def add_bigrams(wordlist):
    for phrase in wordlist:
        words = phrase.split(' ')
        add_relation('bigram', words, phrase, wordlist[phrase])
        logger.info(('bigram', words, phrase, wordlist[phrase]))

