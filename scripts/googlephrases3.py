# Try to find interesting 2- or 3-word phrases.
from solvertools.util import get_datafile, get_dictfile
from solvertools.wordlist import PHRASES, Google1M
from solvertools.wordnet import morphy_roots
import codecs

for line in codecs.open(get_datafile('inputs/3grams-common.txt'), encoding='utf-8'):
    if line.strip():
        listything, occurrences = eval(line.strip())
        assert len(listything) == 3
        groupings = [[listything[0]+' '+listything[1], listything[2]],
                     [listything[1]+' '+listything[2], listything[0]]]
        themax = 0
        for bigram, unigram in groupings:
            for uroot in morphy_roots(unigram, include_self=True):
                for broot in morphy_roots(bigram, include_self=True):
                    themax = max(themax, PHRASES.get(broot, 1000) * Google1M.get(uroot, 0))
        expected_freq = themax/1e20
        if expected_freq > 0:
            freq = occurrences/1e10
            score = freq**1.5 / expected_freq
            phrase = ' '.join(listything)
            if score > 0.00005:
                print "%s,%s" % (phrase, occurrences)
            elif score > 0.00001:
                print "\t%s,%s" % (phrase, occurrences)
