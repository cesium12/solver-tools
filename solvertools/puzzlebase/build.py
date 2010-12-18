from solvertools.puzzlebase.tables import Word, Relation, make_alphagram, commit
from solvertools.wordlist import NPL, ENABLE, WORDNET, PHONETIC, COMBINED_WORDY, CROSSWORD, PHRASES, Wordlist, alphanumeric_only, with_frequency
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

PUZZLEBASE = Wordlist('puzzlebase_current', alphanumeric_only, with_frequency)
def add_concatenations(wordlist):
    counter = 0
    for word in wordlist:
        freq = wordlist[word]
        for prefixlen in xrange(1, len(word)):
            prefix = word[:prefixlen]
            if prefix in wordlist:
                suffix = word[prefixlen:]
                if suffix in wordlist:
                    # to avoid degenerate cases, at least one word must be
                    # valid for Scrabble or a single letter. Or both if
                    # they're really short.
                    score = 0
                    if prefix in ENABLE or len(prefix) == 1: score += 1
                    if suffix in ENABLE or len(suffix) == 1: score += 1
                    if len(prefix) >= 5 or len(suffix) >= 5: score += 1
                    if score >= 2:
                        logger.info("%s (%d) = %s + %s" % (word, wordlist[word], prefix, suffix))
                        counter += 1
                        rel1, rel2 = Relation.make_2way('can_append', 'can_prepend', prefix, suffix)
                        rel1.interestingness = freq
                        rel2.interestingness = freq
        if counter > 1000:
            logger.info("committing")
            commit()
            counter = 0
    commit()

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
    counter = 0
    for phrase in wordlist:
        freq = wordlist[phrase]
        words = phrase.split(' ')
        for offset in xrange(len(words)-1):
            word1 = Word.get(words[offset])
            if word1 is None:
                word1 = Word.make(words[offset], 500, lexical=False)
            word2 = Word.get(words[offset+1])
            if word2 is None:
                word2 = Word.make(words[offset+1], 500, lexical=False)

            rel1, rel2 = Relation.make_2way('precedes', 'follows', word1, word2)
            rel1.interestingness = max(rel1.interestingness, freq)
            rel2.interestingness = max(rel2.interestingness, freq)
            logger.info('precedes(%s, %s)' % (words[0], words[1]))
            counter += 1
            if counter >= 1000:
                logger.info('committing')
                commit()
                counter = 0
    commit()

