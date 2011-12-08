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
from solvertools.anagram.mixmaster import letter_diff
from solvertools.puzzlebase.mongo import DB
import numpy as np

def anahash(word):
    distro = compare_letter_distribution(word)
    return alphagram(''.join(ENGLISH[index] for index in xrange(len(distro)) if distro[index] > 0))

def sorted_diff(text1, text2):
    p1 = p2 = 0
    len1 = len(text1)
    len2 = len(text2)
    out = []
    while p2 < len2:
        if p1 == len1:
            return None
        if text1[p1] == text2[p2]:
            p1 += 1
            p2 += 1
        elif text1[p1] < text2[p2]:
            out.append(text1[p1])
            p1 += 1
        else:
            return None
    out.extend(text1[p1:])
    return ''.join(out)

def parallel(a, b):
    return a*b/(a+b)

def anagram1(text):
    alpha = alphagram(text)
    for entry in DB.alphagrams.find({'alphagram': alpha}).sort([('goodness', -1)]):
        yield entry['text'], entry['freq']

def anagram2(text):
    "Testing for efficiency."
    alpha = alphagram(text)
    ana = list(anahash(text))
    print "anahash:", ana
    nailed_it = False
    for entry in DB.alphagrams.find({'alphagram': alpha}).sort([('goodness', -1)]):
        yield entry['text'], entry['freq']
        nailed_it = True
    if not nailed_it:
        for entry in DB.alphagrams.find({'letters': {'$all': ana}}).sort([('goodness', -1)]):
            diff = sorted_diff(alpha, entry['alphagram'])
            if diff is not None:
                if diff == '':
                    yield entry['text'], entry['freq']
                else:
                    print '\t', entry['text'].lower(), diff
                    for other_piece, other_freq in anagram2(diff):
                        yield entry['text'] + ' ' + other_piece, parallel(entry['freq'], other_freq)

def show_anagrams(text):
    for result, freq in anagram2(text):
        print result, freq
