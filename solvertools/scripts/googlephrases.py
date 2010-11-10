# A quick hacky script to generate google_phrases.txt from Alex's format.
from solvertools.util import get_datafile, get_dictfile
import codecs

thedict = {}
for line in codecs.open(get_datafile('inputs/common_ngrams.txt'), encoding='utf-8'):
    if line.strip():
        listything, freq = eval(line.strip())
        word = ' '.join(listything)
        thedict[word] = freq

words = sorted(thedict.keys())

outfile = codecs.open(get_dictfile('google_phrases.txt'), 'w', encoding='utf-8')
print "Writing:", outfile
for word in words:
    outfile.write("%s,%d\n" % (word, thedict[word]))
    print("%s,%d" % (word, thedict[word]))
outfile.close()

