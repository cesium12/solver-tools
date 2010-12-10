from solvertools.puzzlebase.tables import Word, Relation, make_alphagram, commit
from solvertools.wordlist import NPL, ENABLE, WORDNET, PHONETIC, COMBINED_WORDY, CROSSWORD, PHRASES, PUZZLEBASE
from solvertools.wordnet import morphy_roots
from solvertools.model.tokenize import get_words
from nltk.corpus import wordnet as wn
import logging
import elixir
logger = logging.getLogger(__name__)

# oversimplified rule of thumb: any word that appears 1.3 billion times or more
# on Google is a stopword
STOPWORD_CUTOFF = 1300000000

def initial_setup():
    elixir.create_all()
    elixir.setup_all()
    Word.add_from_wordlist(WORDNET, minimum_freq=20000)
    Word.add_from_wordlist(ENABLE, minimum_freq=2000, scrabble=True)
    Word.add_from_wordlist(NPL, minimum_freq=10000)
    Word.add_from_wordlist(PHONETIC, minimum_freq=10000)
    Word.add_from_wordlist(CROSSWORD, minimum_freq=1000)
    commit()

def advanced_setup():
    Word.add_from_wordlist(WIKIPEDIA, minimum_freq=11000)
    Word.add_from_wordlist(PHRASES, minimum_freq=1000, lexical=False)

def add_roots(wordlist):
    for word in wordlist:
        for lemma in morphy_roots(word):
            if not Word.get(word):
                Word.make(word, 1000)
            Relation.make_2way('has_root', 'has_inflection', word, lemma)
            logger.info('has_root(%s, %s)' % (word, lemma))
    commit()

def show_concatentations(wordlist):
    for word in wordlist:
        for prefixlen in xrange(1, len(word)-1):
            prefix = word[:prefixlen]
            if prefix in wordlist:
                suffix = word[prefixlen:]
                if suffix in wordlist:
                    # to avoid degenerate cases, at least one word must be
                    # valid for Scrabble.
                    if prefix in ENABLE or suffix in ENABLE:
                        print "%s = %s + %s" % (word, prefix, suffix)

def add_clues(mapping):
    """
    Take a word mapping, like CROSSWORD or WORDNET_DEFS. Extract all words
    from the definitions/clues except for very common words such as 'the'.
    Give them the symmetric 'has_clue' relation with the keyword.
    """
    for word in mapping:
        word1 = Word.get(word)
        if not word1: continue
        for clue in mapping[word]:
            clue_words = get_words(clue)
            for clue_word in clue_words:
                possibilities = [clue_word] + list(morphy_roots(clue_word))
                for word2 in possibilities:
                    word2 = Word.get(word2)
                    if not word2: continue
                    if word2.key != word1.key and word2.freq < STOPWORD_CUTOFF:
                        Relation.make_symmetric('has_clue', word1, word2)
                        logger.info('has_clue(%s, %s)' % (word1, word2))
    commit()

def add_bigrams(wordlist):
    for phrase in wordlist:
        words = phrase.split(' ')
        for offset in xrange(len(words)-1):
            word1 = Word.get(words[offset])
            if word1 is None:
                word1 = Word.make(words[offset], 500, lexical=False)
            word2 = Word.get(words[offset+1])
            if word2 is None:
                word2 = Word.make(words[offset+1], 500, lexical=False)

            rel1, rel2 = Relation.make_2way('precedes', 'follows', word1, word2)
            rel1.freq = wordlist[phrase]
            rel2.freq = wordlist[phrase]
            logger.info('precedes(%s, %s)' % (words[0], words[1]))
    commit()

def add_meta_bigrams(wordlist)
    for phrase in wordlist:
        words = phrase.split(' ')
        if len(words) >= 3:
            for split in xrange(1, len(words-1)):
                part1 = Word.get(' '.join(words[:split]))
                part2 = Word.get(' '.join(words[split:]))
                if part1 and part2:
                    rel1, rel2 = Relation.make_2way('precedes', 'follows', word1, word2)
                    rel1.freq = wordlist[phrase]
                    rel2.freq = wordlist[phrase]
                    logger.info('precedes(%s, %s)' % (part1, part2))
    commit()
