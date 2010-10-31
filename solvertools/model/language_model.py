"""
Some NLP code designed to answer the question: "How much does this text look
like reasonable English?"
"""

from solvertools.lib.probability import FreqDist, LidstoneProbDist, \
                                        LaplaceProbDist, MLEProbDist
from solvertools.lib.tokenize import tokenize
from solvertools.model.numbers import number_logprob, is_numeric
from solvertools.model.answer_reader import answer_reader
from solvertools.util import load_pickle, save_pickle, get_picklefile, \
                             file_exists
from solvertools import wordlist
import random, string, logging
logger = logging.getLogger(__name__)

# Loaded language models go here. (TODO: more elegant code for this?)
CACHE = {}

def scan_ngrams(seq, n=2):
    """
    Given a sequence, extract all n-grams of a given length from it.
    """
    for i in xrange(len(seq)-n+1):
        fragment = seq[i:i+n]
        yield fragment

class LanguageModel(object):
    """
    A base class of language models. Right now there's only one subclass,
    but this allows for the possibility of others.
    """
    pass

class WordListModel(LanguageModel):
    """
    A language model that extrapolates from a list of words in that language.

    Given appropriate wordlists, this could easily be extended to other
    languages besides English.
    """
    def __init__(self, name, wordlist):
        if file_exists(get_picklefile(name+'.model.pickle')):
            self._load_from_pickle(name+'.model.pickle')
        else:
            self.wordlist = wordlist
            letter_freq = FreqDist()        # letter unigram frequencies
            bigram_freq = FreqDist()        # letter bigram frequencies
            word_freq = FreqDist()          # word frequencies

            if not wordlist.words: wordlist.load()
            for word, freq in wordlist.iteritems():
                # store the word frequency in the frequency distribution
                word_freq.inc(word, freq)
                for letter in ' '+word:
                    letter_freq.inc(letter)
                for ngram in scan_ngrams(' '+word+' ', 2):
                    # record the n-gram frequencies of letters
                    bigram_freq.inc(ngram, freq)
            
            self.letter_dist = MLEProbDist(letter_freq)
            self.bigram_dist = LidstoneProbDist(bigram_freq, 1000)
            self.word_dist = LaplaceProbDist(word_freq)
            self._save_pickle(name+'.model.pickle')

    def _load_from_pickle(self, filename):
        logger.info('Loading %s' % filename)
        (self.wordlist, self.letter_dist, self.bigram_dist,
        self.word_dist) = load_pickle(filename)
    def _save_pickle(self, filename):
        logger.info('Saving %s' % filename)
        stuff = (self.wordlist, self.letter_dist, self.bigram_dist,
        self.word_dist)
        save_pickle(stuff, filename)
    
    def letters_logprob(self, word):
        """
        Get the relative probability of this word according to the letter
        bigrams in it.
        """
        word = self.wordlist.convert(word)
        logprob = self.letter_dist.logprob(' ')
        if not word: return logprob
        for bigram in scan_ngrams(' '+word+' ', 2):
            # multiply p by the probability of the bigram given its first
            # character
            if bigram[0] in self.letter_dist.freqdist():
                logprob += self.bigram_dist.logprob(bigram)
                logprob -= self.letter_dist.logprob(bigram[0])
        return logprob

    def word_logprob(self, word, fallback_logprob=-35.0):
        """
        Get the relative probability of this word given its appearance in
        a wordlist.
        """
        if is_numeric(word):
            return number_logprob(int(word))
        else:
            if word in self.wordlist:
                return self.word_dist.logprob(self.wordlist.convert(word))
            elif word not in self.wordlist:
                return fallback_logprob + self.letters_logprob(word)

    def text_logprob(self, text, fallback_logprob=-35.0):
        """
        Get the relative probability of a text.
        """
        text = text.replace('-', ' ')
        words = [word for word in tokenize(text).split() if
        self.wordlist.convert(word)]
        logprob = 0.0
        for word in words:
            logprob += self.word_logprob(word, fallback_logprob)
        return logprob

    def text_goodness(self, text):
        """
        Get the overall "goodness" of a text, which adjusts its log probability
        for its length.
        """
        return self.text_logprob(text) / len(text)

def unigram_sampler(model):
    """
    Extract random letters from a unigram distribution.

    This is used for generating negative examples for the answer recognizer.
    """
    p = random.random()
    for let in string.uppercase:
        if let == ' ':
            continue
        p -= model.letter_dist.prob(let)
        if p < 0:
            return let
    return unigram_sampler(model)

def unigram_replace(char, model):
    """
    Given a phrase, replace its alphabetic characters with random letters,
    yielding nonsense that looks like the phrase.
    """
    if char == ' ': return char
    else: return unigram_sampler(model)

def get_english_model():
    """
    Load the cached English language model.
    """
    if 'english' not in CACHE:
        CACHE['english'] = WordListModel('english', wordlist.COMBINED)
    return CACHE['english']

def demo():
    """
    Demonstrate this module's ability to distinguish real Mystery Hunt answers
    from gibberish.
    """
    the_model = get_english_model()
    assert 'AMY' in the_model.wordlist
    results = []
    for year in range(2004, 2009):
        for answer in answer_reader(year):
            results.append((the_model.text_goodness(answer), answer, True))
            fakeanswer = ''.join(unigram_replace(x, the_model) for x in answer)
            results.append((the_model.text_goodness(fakeanswer),
                            fakeanswer, False))
    usefulness = 0.0
    for score, result, good in sorted(results):
        if good:
            usefulness += score
        else:
            usefulness -= score
        print "%s\t%5.5f %s" % (good, score, result)
    print usefulness

if __name__ == '__main__':
    demo()
