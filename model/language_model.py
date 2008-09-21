from probability import *
from collections import defaultdict
import sys, os, string, math, os.path, gzip
import cPickle as pickle

basepath = os.path.normpath( os.path.join( __file__, "..") )
dictpath = os.path.join(basepath, 'dict')
sys.path.append(os.path.normpath(os.path.join(basepath, '..')))
from sagesutil import export, data_file
from answer_reader import answer_reader

def scan_ngrams(text, n=2):
    for i in xrange(len(text)-n+1):
        fragment = text[i:i+n]
        yield fragment

class LanguageModel(object):
    """
    A language model suitable for use in metasolve.
    """
    def __init__(self):
        # These dictionaries will be indexed by the number n in
        # the n-grams: 2 for bigrams, 3 for trigrams, etc.

        # The _freq dictionaries track the observed frequencies.
        # The _dist dictionaries smooth these into probability distributions.

        self.wordlist = set()
        self.letter_freq = defaultdict(FreqDist)
        self.word_freq = defaultdict(FreqDist)
        self.letter_dist = {}
        self.word_dist = {}
    
    def learnLetters(self, word, letter_n=3):
        """Learn the letter n-gram frequencies from a word."""
        for n in range(1, letter_n+1):   # current n
            for ngram in scan_ngrams(word, n):
                self.letter_freq[n].inc(ngram)

    def learnWords(self, words, word_n=2, letter_n=3):
        """Take in a generator of words, and learn from it."""
        wordHistory = ()
        counter = 0
        print 'om'
        for word in words:
            counter += 1
            if counter % 10000 == 0: print 'nom'
            word = word.lower()
            self.wordlist.add(word)
            wordHistory = wordHistory[0:word_n-1] + (word,)
            for n in range(1, min(word_n, len(wordHistory))+1):
                ngram = wordHistory[-n:]
                self.word_freq[n].inc(ngram)
            self.learnLetters(word, letter_n)
        print

    def all_words(self):
        return self.wordlist

    def finalize(self):
        for key in self.letter_freq:
            self.letter_dist[key] = LaplaceProbDist(self.letter_freq[key])
        for key in self.word_freq:
            self.word_dist[key] = LidstoneProbDist(self.word_freq[key], 0.1)
    
    def letters_logprob(self, word):
        logprob = count = 0
        for n, probdist in self.letter_dist.items():
            for ngram in scan_ngrams(word, n):
                logprob += probdist.logprob(ngram)
                count += 1
        return logprob/count

    def words_logprob(self, words, ngram_logprob=-10):
        words = tuple(words)
        logprob = 0
        for n, probdist in self.word_dist.items():
            for ngram in scan_ngrams(words, n):
                lp = probdist.logprob(ngram)
                if n == 1:
                    lp_ngram = self.letters_logprob(ngram[0])
                    lp += lp_ngram
                logprob += lp
        return logprob

    def text_logprob(self, text, ngram_logprob=-10):
        return self.words_logprob(text.lower().split(), ngram_logprob)

    def given_logprob(self, word, context, ngram_logprob=-10):
        return (self.words_logprob(tuple(context)+(word,), ngram_logprob) -
                self.words_logprob(context, ngram_logprob))
    
    # This one is compatible with metasolve
    def prob(self, word, context=[]):
        word = word.lower()
        context = [w.lower() for w in context]
        return math.pow(2, self.given_logprob(word, context))

def get_english_model():
    from nltk.corpus import brown
    model = LanguageModel()
    
    f = open(os.path.join(dictpath, 'enable.txt'))
    enable = [line.strip().lower() for line in f]
    f.close()
    
    model.learnWords(brown.words(), word_n=1)
    model.learnWords(enable, word_n=1)
    model.finalize()
    return model

english_pickle = os.path.join(basepath, 'pickle', 'english.model.pickle.gz')
if os.access(english_pickle, os.F_OK):
    f = gzip.open(english_pickle)
    english_model = pickle.load(f)
    f.close()
else:
    print "Generating English model: english.model.pickle.gz."
    english_model = get_english_model()
    out = gzip.open(english_pickle, 'w')
    pickle.dump(english_model, out)
    out.close()

english_model.finalize()
if __name__ == '__main__':
    results = []
    for year in range(2004, 2009):
        for answer in answer_reader(year):
            results.append((english_model.text_logprob(answer)/len(answer.split()), answer))
    for score, result in sorted(results):
        print "%5.5f %s" % (score, result)
