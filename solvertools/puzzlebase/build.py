from solvertools.puzzlebase.tables import Word, Relation, session, make_alphagram
from solvertools.wordlist import COMBINED_WORDY
from nltk.corpus import wordnet as wn
import logging
logger = logging.getLogger(__name__)

def initial_setup():
    elixir.setup_all()
    elixir.create_all()
    Word.build_table()

def morphy_lemmas(word):
    wnword = word.lower().replace(' ', '_')
    lemmas = set()
    for pos in 'vna':
        lemma = wn.morphy(wnword, pos)
        if lemma is not None and lemma != wnword:
            lemmas.add(lemma.replace('_', ' ').upper())
    return lemmas

def add_lemmas():
    for word in COMBINED_WORDY:
        for lemma in morphy_lemmas(word):
            Relation.make_2way('has_root', 'has_inflection', word, lemma)
            logger.info('has_root(%s, %s)' % (word, lemma))
    session.commit()

def add_anagrams():
    for word in COMBINED_WORDY:
        word1 = Word.get(word)
        others = Word.query.filter_by(alphagram=word1.alphagram)
        for word2 in others:
            if word2.key != word1.key:
                Relation.make('has_anagram', word1, word2)
                logger.info('has_anagram(%s, %s)' % (word1.key, word2.key))
    session.commit()

