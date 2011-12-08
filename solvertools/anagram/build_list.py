from solvertools.anagram.anahash import anahash, alphagram

def make_anagram_list(wordlist, filename):
    out = open(filename, 'w')
    for word in wordlist:
        freq = wordlist[word]
        ahash = anahash(word)
        alph = alphagram(word)
        print >> out, "%s\t%s\t%s\t%s" % (ahash, alph, word, freq)


