from bayesinator.core import *
import math

_dictionary = {}
_total_freq = 0

for line in open('data/dict/google200K.txt'):
    [word, freq] = line.split(',')
    word = word.upper()
    freq = int(freq)
    if freq <= 0:
        continue
    if word in _dictionary:
        _dictionary[word] += freq
    else:
        _dictionary[word] = freq
    _total_freq += freq

@puzzle_property(str)
def word(s):
    return s.upper() in _dictionary

@entropy_function(word)
def word_entropy(word):
    return math.log(float(_total_freq) / _dictionary[word.upper()], 2)
