from solvertools.wordlist import *
from solvertools.util import *

# I don't understand why sages_combined ended up with things that were missing
# from sages_combined2, but both of them were made by kind of messy processes.
# Time to fix this.

in1 = open(get_dictfile('sages_combined.txt'))
in2 = open(get_dictfile('sages_combined2.txt'))
out = open(get_dictfile('sages_combined_final.txt'), 'w')

words = {}
for line in in1:
    word,freq = line.strip().rsplit(',',1)
    freq = int(freq)
    key = alphanumeric_only(word)
    if key not in words:
        words[key] = (word, freq)
        print 'read', key, freq

for line in in2:
    word,freq = line.strip().rsplit(',',1)
    freq = int(freq)
    key = alphanumeric_only(word)
    if key not in words:
        words[key] = (word, freq)
        print 'read', key, freq
    elif words[key][1] < freq:
        words[key] = (words[key][0], freq)
        print 'incremented', key, freq

results = words.values()
results.sort(key=lambda x: (-x[1], x[0]))
for word, freq in results:
    print "%s,%d" % (word, freq)
    print >> out, "%s,%d" % (word, freq)
out.close()

