from solvertools.puzzlebase.mongo import add_from_wordlist, add_relation, add_word, DB
from solvertools.wordlist import NPL, ENABLE, WORDNET, PHONETIC, COMBINED_WORDY, CROSSWORD, PHRASES, WIKIPEDIA, WIKTIONARY, WIKTIONARY_DEFS, WORDNET_DEFS, Google200K, alphagram
from solvertools.wordnet import morphy_roots
from solvertools.model.tokenize import get_words
from solvertools.util import get_dictfile
from math import log
import logging
logger = logging.getLogger(__name__)

# oversimplified rule of thumb: any word that appears 1.3 billion times or more
# on Google is a stopword
STOPWORD_CUTOFF = 1300000000

def initial_setup():
    # comments with num? indicate how much I wish I had run it at.
    #
    # Google1M was killed at a minimum of 6255 because everything sucks long
    # before then.
    add_from_wordlist(ENABLE, multiplier=2000)
    add_from_wordlist(NPL, multiplier=5000, lexical=False)
    add_from_wordlist(PHONETIC, multiplier=10000)
    add_from_wordlist(CROSSWORD, multiplier=100, lexical=False)
    add_from_wordlist(WIKIPEDIA, multiplier=5000) # 20000?
    add_from_wordlist(WORDNET, multiplier=10000) # 40000?
    add_from_wordlist(WIKTIONARY, multiplier=2000) # 30000?
    add_from_wordlist(Google1M, lexical=False)
    add_from_wordlist(PHRASES, lexical=False)

def more_setup():
    add_roots(WORDNET)
    add_bigrams(WORDNET)
    add_bigrams(NPL)
    add_bigrams(PHRASES)
    add_clues(CROSSWORD)
    add_clues(WIKTIONARY_DEFS)
    add_clues(WORDNET_DEFS)
    add_concatenations(ENABLE)

def add_roots(wordlist):
    for word in wordlist:
        for lemma in morphy_roots(word):
            add_relation('has_root', [word, lemma])
            logger.info(('has_root', [word, lemma]))

def add_concatenations(wordlist, base_wordlist=None, dryrun=False):
    if base_wordlist is None:
        base_wordlist = wordlist
    for word in wordlist:
        freq = wordlist[word]
        for prefixlen in xrange(1, len(word)):
            prefix = word[:prefixlen]
            if prefix in base_wordlist or len(prefix) == 1:
                suffix = word[prefixlen:]
                if suffix in base_wordlist or len(suffix) == 1:
                    if not dryrun:
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
                if clue_word != '=>':
                    possibilities = [clue_word] + list(morphy_roots(clue_word))
                    for word2 in possibilities:
                        add_relation('clued_by', [word, word2])
                        logger.info(('clued_by', [word, word2]))

def add_bigrams(wordlist):
    for phrase in wordlist:
        words = [w for w in phrase.split(' ') if w.upper() != 'AND']
        if len(words) == 2:
            add_relation('bigram', words, phrase, wordlist[phrase])
            logger.info(('bigram', words, phrase, wordlist[phrase]))

def fix_words():
    """
    This will re-count the word frequencies based on the alphagram frequencies.
    """
    out = open(get_dictfile('puzzlebase_current.txt'), 'w')
    for rec in DB.alphagrams.find():
        text = rec['text']
        freq = rec['freq']
        add_word(text, freq)
        print >> out, "%s,%s" % (text, freq)
        logger.info((text, freq))

def add_interestingness(rel_type):
    for entry in DB.relations.find({'rel': rel_type}):
        rel = entry['rel']
        rel_total = 0.0
        words = entry['words']
        if len(words) < 2:
            print 'not enough words', words
            continue
        for word in words:
            key = rel+' '+word
            rel_total += log(DB.totals.find_one({'_id': key})['value']['total'])
        interestingness = log(entry['freq']+1) - rel_total/len(words)
        DB.relations.update(
            {'_id': entry['_id']},
            {'$set': {'interestingness': interestingness}}
        )
        logger.info((rel, words, interestingness))

def export_clues(filename):
    out = open(filename, 'w')
    for entry in DB.relations.find({'rel': {'$in': ['clued_by', 'bigram', 'can_adjoin', 'has_root']}}):
        print >> out, ('%s\t%s\t%s' % (entry['freq'], entry['words'][0], entry['words'][1])).encode('utf-8')

def clue_matrix(filename):
    import divisi2
    clue_entries = []
    for line in open(filename):
        val, row, col = line.strip().split('\t')
        val = 1
        clue_entries.append((val, row, col))
        if len(clue_entries) % 10000 == 0:
            print len(clue_entries)
    sparse = divisi2.SparseMatrix.square_from_named_entries(clue_entries)
    return sparse

