# Try to find interesting 2- or 3-word phrases.
from solvertools.util import get_datafile, get_dictfile
from solvertools.wordlist import Google1M
from solvertools.wordnet import morphy_roots
import codecs

for line in codecs.open(get_datafile('inputs/3grams-common.txt'), encoding='utf-8'):
    if line.strip():
        listything, occurrences = eval(line.strip())
        expected_freq = 1.0
        for word in listything:
            themax = 0
            for root in morphy_roots(word, include_self=True):
                themax = max(themax, Google1M.get(root))
            expected_freq *= themax/1e10
        if expected_freq > 0:
            freq = occurrences/1e10
            score = freq**2.5 / expected_freq
            phrase = ' '.join(listything)
            if score > .0001:
                print "%s,%s,%s" % (phrase, occurrences, score)
            elif score > .00005:
                print "\t* %s,%s,%s" % (phrase, occurrences, score)
