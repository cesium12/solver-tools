from solvertools.puzzlebase.tables import Word, Relation, make_alphagram, commit
from solvertools.wordlist import NPL, ENABLE, WORDNET, PHONETIC, COMBINED_WORDY, CROSSWORD
from solvertools.wordnet import morphy_roots
from nltk.corpus import wordnet as wn
import logging
import elixir
logger = logging.getLogger(__name__)

def initial_setup():
    elixir.create_all()
    elixir.setup_all()
    Word.add_from_wordlist(WORDNET, minimum_freq=20000)
    Word.add_from_wordlist(ENABLE, minimum_freq=2000, scrabble=True)
    Word.add_from_wordlist(NPL, minimum_freq=10000)
    Word.add_from_wordlist(PHONETIC, minimum_freq=10000)
    Word.add_from_wordlist(CROSSWORD, minimum_freq=1000)
    commit()

def add_roots():
    for word in COMBINED_WORDY:
        for lemma in morphy_roots(word):
            if not Word.get(word):
                Word.make(word, 1000)
            Relation.make_2way('has_root', 'has_inflection', word, lemma)
            logger.info('has_root(%s, %s)' % (word, lemma))
    commit()

def add_anagrams():
    for word in COMBINED_WORDY:
        word1 = Word.get(word)
        if not word1: continue
        if len(word1.key) < 5: continue
        others = Word.query.filter_by(alphagram=word1.alphagram)
        for word2 in others:
            if word2.key != word1.key:
                Relation.make('has_anagram', word1, word2)
                logger.info('has_anagram(%s, %s)' % (word1.key, word2.key))
    commit()

