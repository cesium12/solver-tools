from probability import *
from collections import defaultdict
import sys, os, string, math, os.path
import cPickle as pickle

basepath = os.path.normpath( os.path.join( __file__, "..") )
dictpath = os.path.join(basepath, 'dict')
sys.path.append(os.path.normpath(os.path.join(basepath, '..')))
from sagesutil import export

ngrams = defaultdict(dict)
words = {}
wordlists = {}

ngrams['English'][1] = DictionaryProbDist(dict(a=8.167, b=1.492, c=2.782,
d=4.253, e=12.702, f=2.228, g=2.015, h=6.094, i=6.996, j=0.153, k=0.772,
l=4.025, m=2.406, n=6.749, o=7.507, p=1.929, q=0.095, r=5.987, s=6.327,
t=9.056, u=2.758, v=0.978, w=2.360, x=0.150, y=1.974, z=0.074), normalize=True)

f = open(os.path.join(dictpath, 'all.txt'))
wordlists['npl'] = [line.strip().lower() for line in f]
f.close()

f = open(os.path.join(dictpath, 'enable.txt'))
wordlists['enable'] = [line.strip().lower() for line in f]
f.close()

english_ngrams_pickle = os.path.join(basepath, 'pickle', 'english.ngrams.pickle')
if os.access(english_ngrams_pickle, os.F_OK):
    f = open(english_ngrams_pickle)
    ngrams['English'] = pickle.load(f)
    f.close()
else:
    print "Collecting English bigrams and trigrams: english.ngrams.pickle."
    from nltk.corpus import brown
    bigramdist = FreqDist()
    trigramdist = FreqDist()
    for word in brown.words():
        word = ''.join(let for let in word.lower() if let in string.letters)
        for i in xrange(len(word)-1):
            bigramdist.inc(word[i:i+2])
        for i in xrange(len(word)-2):
            trigramdist.inc(word[i:i+3])
    f = open(english_ngrams_pickle, 'w')
    ngrams['English'][2] = LaplaceProbDist(bigramdist)
    ngrams['English'][3] = LaplaceProbDist(trigramdist)
    pickle.dump(ngrams['English'], f)
    f.close()

english_words_pickle = os.path.join(basepath, 'pickle', 'english.words.pickle')
if os.access(english_words_pickle, os.F_OK):
    f = open(english_words_pickle)
    words['English'] = pickle.load(f)
    f.close()
else:
    print "Collecting English words: english.words.pickle."
    from nltk.corpus import brown
    worddist = FreqDist()
    for word in brown.words():
        word = ''.join(let for let in word.lower() if let in string.letters)
        worddist.inc(word)
    for word in wordlists['npl']:
        worddist.inc(word)
    for word in wordlists['enable']:
        worddist.inc(word, 2)
    f = open(english_words_pickle, 'w')
    words['English'] = MLEProbDist(worddist)
    pickle.dump(words['English'], f)
    f.close()

def scan_ngrams(text, n=2):
    text = text.lower()
    for i in xrange(len(text)-n+1):
        fragment = text[i:i+n]
        if fragment[0] in string.letters and fragment[1] in string.letters:
            yield fragment

@export(description="""An estimated probability that this word would appear
as a word of natural language.""",
  args=["The word to test", "The language model to use (default is 'English')"],
  ret="The log likelihood of the word in the language model")
def word_likelihood(word, lang='English', ngram_prob=0.001):
    """
    Look up a word in both the word frequency distribution and the ngram
    frequency distribution (to account for unknown words).
    """
    actual_word_likelihood = 1-ngram_prob
    logprob = words[lang].logprob(word) + math.log(actual_word_likelihood, 2)
    if logprob <= -1e300:
        logprob = math.log(ngram_prob, 2)
        for bigram in scan_ngrams(word, 2):
            logprob += ngrams[lang][2].logprob(bigram)
        for trigram in scan_ngrams(word, 3):
            logprob += ngrams[lang][3].logprob(trigram)
    return logprob

def text_likelihood(text, lang='English', ngram_prob=0.001, good_words=[]):
    text = ''.join(let for let in text.lower() if let in string.letters+' ')
    total = 0.0
    for word in text.split():
        if word in good_words:
            total += 3
        else:
            total += word_likelihood(word, lang, ngram_prob)
    return total

if __name__ == '__main__':
    print "Demo:"
    for word in ['the', 'cat', 'spatula', 'huzzah', 'defenestrate',
    'adogslife', 'cka', 'splendiferosity', 'qejvkobckh']:
        print "Word: %s\tLog likelihood: %3.3f" % (word, word_likelihood(word))

