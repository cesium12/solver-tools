from numpy import *
from math import log
from string import letters, uppercase

distro = {}

# There's always the possibility that you have random crap.
distro['uniform'] = ('Uniform distribution', 1.0, ones(26)/26)

# Distribution of running English text, according to
# http://www.csm.astate.edu/~rossa/datasec/frequency.html. This is slightly
# different from the distribution of English letters in arbitrary words.
distro['english-sent'] = ('English sentences', 6.0, array([
  8.167, 1.492, 2.782, 4.253,12.702, 2.228, 2.015, 6.094, 6.996, 0.153,
  0.772, 4.025, 2.406, 6.749, 7.507, 1.929, 0.095, 5.987, 6.327, 9.056,
  2.758, 0.978, 2.360, 0.150, 1.974, 0.074])/100)

# If you get a Zipf's law (1/n) distribution, then there's some information
# content, but it may not be letters. This distribution is intended to
# represent the aggregate of all unknown sources of data.
zipfdist = ones(26)/range(2, 28)
zipfdist /= sum(zipfdist)
distro['zipf'] = ("Other data source", 4.0, zipfdist)

def letter_add(c, n):
    if c not in letters: return c
    val = ord(c) % 32
    newval = (val+n) % 26
    if newval == 0: newval = 26
    return chr(64+newval)

def caesar_shift(text, n):
    return ''.join(letter_add(c, n) for c in text)

def caesar_likelihood(text, dist, n):
    return likelihood(caesar_shift(text, n), dist)
    
def likelihood(text, dist):
    loglike = 0.0
    for ch in text:
        if ch in letters:
            val = (ord(ch) % 32) - 1
            loglike += log(dist[val])
    return loglike

## This would work if it didn't subtract the odd permutations from the
## even ones...
#def crypto_likelihood(text, dist):
#    matrix = ones((26, 26))
#    for ch in text:
#        if ch in letters:
#            val = (ord(ch) % 32) - 1
#            matrix[val] *= (dist * 26.0)
#    determinant = linalg.det(matrix)
#    print matrix
#    return log(determinant) - 26*log(26)

def crypto_solve(text, dist):
    freq = zeros(26)
    for ch in text:
        if ch in letters:
            val = (ord(ch) % 32) - 1
            freq[val] += 1
    order_freq = zip(list(freq), uppercase)
    order_freq.sort()
    order_freq.reverse()

    order_dist = zip(list(dist), uppercase)
    order_dist.sort()
    order_dist.reverse()
    
    loglike = 0.0
    decode = {}
    n = len([ch for ch in text if ch in letters])
    for (fpair, ppair) in zip(order_freq, order_dist):
        f, flet = fpair
        p, plet = ppair
        loglike += f * log(p)
        decode[flet] = plet
    #decoded = ''.join(decode.get(ch, ch) for ch in text.upper())
    return (loglike, None)

def analyze(text):
    # Relative probabilities of each kind of transformation
    fprior = {}
    fprior['identity'] = 1.0
    # Cryptograms become more likely as the text gets longer
    fprior['cryptogram'] = 1.0 * len(text) / ((400.0/len(text)) + len(text))
    fprior['caesar'] = 1.0 * (400.0/len(text)) / (400.0/len(text) + len(text))
    
    results = []
    for key, dist in distro.items():
        # Each distribution contains a name, an estimated prior probability
        # that the data fits that distribution, and a probability distribution
        # over 26 letters.
        name, dprior, probdist = dist
        if key != 'zipf':
            results.append( (name, 'identity', None,
                         likelihood(text, probdist) + log(fprior['identity'])
                         + log(dprior)))
        if key != 'uniform' and key != 'zipf':
            for n in range(0, 26):
                results.append( (name, 'caesar', (26-n),
                                 caesar_likelihood(text, probdist, n) +
                                 log(fprior['caesar']) + log(dprior)
                                 - log(26)))
        if key != 'uniform':
            crypto_likelihood, crypto_guess = crypto_solve(text, probdist)
            results.append( (name, 'cryptogram', crypto_guess,
                             crypto_likelihood + log(fprior['cryptogram'])
                             + log(dprior) - 10*log(10)))

    results.sort(cmp=(lambda a,b: cmp(a[3], b[3])))
    results.reverse()
    return results

def main():
    text = raw_input('Enter text to decrypt: ')
    results = analyze(text)

    for res in results[:5]:
        distname, transform, param, loglike = res
        print loglike, '\t', distname, transform, param
        cleartext = ''
        if transform == 'caesar': cleartext = caesar_shift(text, (26-param))
        elif transform == 'identity': cleartext = text
        if distname in ["Uniform distribution", "Other data source"]:
            cleartext = ''
        print cleartext
        print
    
if __name__ == '__main__': main()

