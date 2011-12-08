"""
An "anahash" is a signature of a set of letters for anagramming, indicating
which letters it contains more of than the average English word.

When anagramming a large set of letters that does not resolve to a single
word or phrase, then a plausible sub-anagram will be one whose anahash is a
substring of the letters' anahash.

This is not true of *all* sub-anagrams, but if an anagram falls apart into two
or more phrases, usually at least one of them will have this reasonable
property.

For short words and phrases, the anahash will simply be the set of letters they
contain. For longer phrases, common letters do not appear if they are
infrequent; for example, "e" is not in the anahash of
"supercalifragilisticexpialidocious", because two Es in 34 letters is not very
many.
"""
from solvertools.letter_stats import compare_letter_distribution
from solvertools.alphabet import ENGLISH
from solvertools.wordlist import alphagram
import numpy as np

def anahash(word):
    distro = compare_letter_distribution(word)
    return alphagram(''.join(ENGLISH[index] for index in xrange(len(distro)) if distro[index] > 0))

