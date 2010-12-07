from solvertools.puzzlebase.tables import Word, Relation, make_alphagram, commit
from solvertools.wordlist import NPL, ENABLE, WORDNET, PHONETIC, COMBINED_WORDY, CROSSWORD
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

def add_roots(wordlist):
    for word in wordlist:
        for lemma in morphy_roots(word):
            if not Word.get(word):
                Word.make(word, 1000)
            Relation.make_2way('has_root', 'has_inflection', word, lemma)
            logger.info('has_root(%s, %s)' % (word, lemma))
    commit()

def add_anagrams(wordlist):
    for word in wordlist:
        word1 = Word.get(word)
        if not word1: continue
        if len(word1.key) < 5: continue
        others = Word.query.filter_by(alphagram=word1.alphagram)
        for word2 in others:
            if word2.key != word1.key:
                Relation.make('has_anagram', word1, word2)
                logger.info('has_anagram(%s, %s)' % (word1.key, word2.key))
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
    for phrase in wordlist:
        words = phrase.split(' ')
        if len(words) == 2:
            rel1, rel2 = Relation.make_2way('precedes', 'follows', words[0], words[1])
            rel1.freq = wordlist[phrase]
            rel2.freq = wordlist[phrase]
            logger.info('precedes(%s, %s)' % (words[0], words[1]))
    commit()
