# A quick hacky script to generate google_phrases.txt from Alex's format.
from solvertools.util import get_datafile, get_dictfile
from solvertools.wordlist import Google200K
import codecs

thedict = {}
for line in codecs.open(get_datafile('inputs/2grams.txt'), encoding='utf-8'):
    if line.strip():
        listything, freq = eval(line.strip())
        expected_freq = 1e-13
        for word in listything:
            expected_freq *= (10000 + Google200K.get(word, 0))
        phrase = ' '.join(listything)
        if freq > expected_freq*1000:
            thedict[phrase] = int(freq/expected_freq)
            print phrase, int(freq/expected_freq)

words = sorted(thedict.keys())

outfile = codecs.open(get_dictfile('google_phrases.txt'), 'w', encoding='utf-8')
print "Writing:", outfile
for word in words:
    outfile.write("%s,%d\n" % (word, thedict[word]))
    print("%s,%d" % (word, thedict[word]))
outfile.close()

