from solvertools.lib.probability import FreqDist, LidstoneProbDist, LaplaceProbDist, MLEProbDist
from solvertools.lib.tokenize import tokenize
from solvertools.model.numbers import number_logprob, is_numeric
from solvertools.model.answer_reader import answer_reader
from solvertools.util import load_pickle, save_pickle, get_picklefile, file_exists
from solvertools import wordlist
import random, string, logging
logger = logging.getLogger('model.language_model')

def scan_ngrams(seq, n=2):
    for i in xrange(len(seq)-n+1):
        fragment = seq[i:i+n]
        yield fragment

class LanguageModel(object):
    # Allowing for the possibility of other language models
    pass

class WordListModel(LanguageModel):
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
        if is_numeric(word):
            return number_logprob(int(word))
        else:
            if word in self.wordlist:
                return self.word_dist.logprob(self.wordlist.convert(word))
            elif word not in self.wordlist:
                return fallback_logprob + self.letters_logprob(word)

    def text_logprob(self, text, fallback_logprob=-35.0):
        text = text.replace('-', ' ')
        words = [word for word in tokenize(text).split() if
        self.wordlist.convert(word)]
        logprob = 0.0
        for word in words:
            logprob += self.word_logprob(word, fallback_logprob)
        return logprob

def unigram_sampler(model):
    p = random.random()
    for let in string.uppercase:
        if let == ' ': continue
        p -= model.letter_dist.prob(let)
        if p < 0: return let
    return unigram_sampler(model)

def unigram_replace(char, model):
    if char == ' ': return char
    else: return unigram_sampler(model)

def getEnglishModel():
    return WordListModel('english', wordlist.COMBINED)

def demo():
    theModel = getEnglishModel()
    assert 'AMY' in theModel.wordlist
    results = []
    for year in range(2004, 2009):
        for answer in answer_reader(year):
            results.append((theModel.text_logprob(answer)/len(answer),
            answer, True))
            fakeanswer = ''.join(unigram_replace(x, theModel) for x in
            answer)
            results.append((theModel.text_logprob(fakeanswer) / 
                            len(fakeanswer), fakeanswer, False))
    usefulness = 0.0
    for score, result, good in sorted(results):
        if good: usefulness += score
        else: usefulness -= score
        print "%s\t%5.5f %s" % (good, score, result)
    print usefulness

if __name__ == '__main__': demo()
