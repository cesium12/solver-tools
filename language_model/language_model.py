from nltk.probability import *
from collections import defaultdict
import sys, os, string, math
import cPickle as pickle

ngrams = defaultdict(dict)
words = {}
wordlists = {}

ngrams['English'][1] = DictionaryProbDist(dict(a=8.167, b=1.492, c=2.782,
d=4.253, e=12.702, f=2.228, g=2.015, h=6.094, i=6.996, j=0.153, k=0.772,
l=4.025, m=2.406, n=6.749, o=7.507, p=1.929, q=0.095, r=5.987, s=6.327,
t=9.056, u=2.758, v=0.978, w=2.360, x=0.150, y=1.974, z=0.074), normalize=True)

f = open('all.txt')
wordlists['npl'] = [line.strip().lower() for line in f]
f.close()

f = open('enable.txt')
wordlists['enable'] = [line.strip().lower() for line in f]
f.close()

if os.access('english.2g.pickle', os.F_OK):
    f = open('english.2g.pickle')
    ngrams['English'][2] = pickle.load(f)
    f.close()
else:
    print "Collecting English bigrams: english.2g.pickle."
    from nltk.corpus import brown
    bigrams = FreqDist()
    for word in brown.words():
        word = ''.join(let for let in word.lower() if let in string.letters)
        for i in xrange(len(word)-1):
            bigrams.inc(word[i:i+2])
    f = open('english.2g.pickle', 'w')
    ngrams['English'][2] = LaplaceProbDist(bigrams)
    pickle.dump(ngrams['English'][2], f)
    f.close()

if os.access('english.words.pickle', os.F_OK):
    f = open('english.words.pickle')
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
        word = line.strip().lower()
        worddist.inc(word)
    for word in wordlists['enable']:
        word = line.strip().lower()
        worddist.inc(word)
    f = open('english.words.pickle', 'w')
    words['English'] = MLEProbDist(worddist)
    pickle.dump(words['English'], f)
    f.close()

def bigrams(text):
    text = text.lower()
    for i in xrange(len(text)-1):
        fragment = text[i:i+2]
        if fragment[0] in string.letters and fragment[1] in string.letters:
            yield fragment

def word_prob(word, lang='English', bigram_prob=0.0005):
    """
    Look up a word in both the word frequency distribution and the bigram
    frequency distribution (to account for unknown words).
    """
    actual_word_prob = 1-bigram_prob
    logprob = words[lang].logprob(word) + math.log(actual_word_prob)
    bigramdist = ngrams[lang][2]
    if logprob <= -1e300:
        logprob = math.log(bigram_prob)
        for bigram in bigrams(word): logprob += bigramdist.logprob(bigram)
    return logprob

print word_prob('the')
print word_prob('spatula')
print word_prob('defenestrate')
print word_prob('splendiferosity')
print word_prob('qejvkobckh')

if __name__ == '__main__':
    print "Demo:"
    for word in ['the', 'spatula', 'defenestrate', 'splendiferosity',
    'qejvkobckh']:
    print "Word: %s\tLog probability: %3.3f" % (word, word_prob(word))

