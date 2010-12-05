# Try to find interesting 2-word phrases.
from solvertools.util import get_datafile, get_dictfile
from solvertools.puzzlebase.tables import *
import codecs

for line in codecs.open(get_datafile('inputs/2grams.txt'), encoding='utf-8'):
    if line.strip():
        listything, occurrences = eval(line.strip())
        expected_freq = 1.0
        for word in listything:
            entry = Word.get(word)
            if entry is None:
                expected_freq = 0
                break
            else:
                expected_freq *= entry.freq/1e10
        if expected_freq > 0:
            freq = occurrences/1e10
            phrase = ' '.join(listything)
            if freq > expected_freq:
                print phrase, freq/expected_freq

