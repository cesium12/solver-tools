# A quick hacky script to generate google1M.txt from Alex's format.
from solvertools.util import get_datafile, get_dictfile
import codecs

thedict = {}
for line in codecs.open(get_datafile('inputs/1grams.txt'), encoding='utf-8'):
    if line.strip():
        listything, freq = eval(line.strip())
        if freq > 30000:
            word = listything[0]
            thedict[word] = freq

cutoff2 = sorted(thedict.values())[-200000]
words = sorted(thedict.keys())

for filename, cutoff in [('google200K.txt', cutoff2)]:
    outfile = codecs.open(get_dictfile(filename), 'w', encoding='utf-8')
    print "Writing:", outfile
    for word in words:
        if thedict[word] >= cutoff:
            outfile.write("%s,%d\n" % (word, thedict[word]))
            print("%s,%d" % (word, thedict[word]))
    outfile.close()

