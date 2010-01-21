# A quick hacky script to generate google1M.txt from Alex's format.
from solvertools.util import get_datafile, get_dictfile
import codecs

thedict = {}
for line in codecs.open(get_datafile('inputs/1grams.txt'), encoding='utf-8'):
    if line.strip():
        listything, freq = eval(line.strip())
        word = listything[0]
        thedict[word] = freq

cutoff = sorted(thedict.values())[-1000000]
words = sorted(thedict.keys())

outfile = codecs.open(get_dictfile('google1M.txt'), 'w', encoding='utf-8')
for word in words:
    if thedict[word] >= cutoff:
        outfile.write("%s,%d\n" % (word, thedict[word]))
        print("%s,%d" % (word, thedict[word]))
outfile.close()

