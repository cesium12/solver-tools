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
import math
import numpy as np

def log2(x):
    return math.log(x) / math.log(2)

def anahash(word):
    if word == '':
        return ''
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
    """
    Get all reasonable 2-part anagrams for the given text, yielding them as they are
    found.
    """
    alpha = alphagram(text)
    ana = anahash(text)
    nailed_it = False
    for entry in DB.alphagrams.find({'alphagram': alpha}).sort([('goodness', -1)]):
        yield entry['text'], entry['freq']
        nailed_it = True
    for result in anagram1(alpha):
        yield result
    for result in _anagram_search(alpha, '', ana):
        yield result

def _anagram_search(alpha, ana, possible):
    first_result = True
    if ana:
        for entry in DB.alphagrams.find({'anahash': {'$gte': ana}}).limit(20):
            if entry['anahash'] != ana:
                if first_result and not entry['anahash'].startswith(ana):
                    return
                else:
                    break
            first_result = False
            diff = sorted_diff(alpha, entry['alphagram'])
            if diff is not None:
                if diff == '':
                    yield entry['text'], entry['freq']
                else:
                    for other_piece, other_freq in anagram1(diff):
                        yield entry['text'] + ' ' + other_piece, parallel(entry['freq'], other_freq)
                        break
    for pos in xrange(len(possible)):
        for result in _anagram_search(alpha, ana+possible[pos], possible[pos+1:]):
            yield result

MAX_FREQ = 42
def anagram_breadth_first(text):
    """
    Searches breadth-first for anagrams with three or more pieces.

    I recommend against actually using this. --Rob
    """
    start_alpha = alphagram(text)
    start_ana = anahash(text)
    queue = [(0.0, start_alpha, '', start_ana, ())]
    while queue:
        score, alpha, ana, rest, sofar = queue.pop()
        dead_end = False
        if alpha == '':
            yield sofar, score
        elif ana:
            first_result = True
            limit = max(int(100 / (0-min(score, -1))), 1)
            for entry in DB.alphagrams.find({'anahash': {'$gte': ana}}).limit(limit):
                if entry['anahash'] != ana:
                    if first_result and not entry['anahash'].startswith(ana):
                        dead_end = True
                    break
                newscore = score + entry['goodness'] - MAX_FREQ
                if len(queue) > 1000 and newscore < queue[-1000][0]:
                    continue
                first_result = False
                diff = sorted_diff(alpha, entry['alphagram'])
                if diff is not None:
                    print '\t', len(queue), '(%s)' % ana, sofar, '/', entry['text'], diff.lower(), newscore
                    for text, freq in anagram1(diff):
                        newnewscore = newscore + log2(freq) - MAX_FREQ
                        yield sofar + (entry['text'], text), newscore
                        break
                    else:
                        if len(queue) < 10000:
                            queue.append((newscore, diff, '', anahash(diff),
                                          sofar+(entry['text'],)))

        if rest and not dead_end:
            for pos in xrange(len(rest)):
                #print '\t', ana+rest[pos]
                queue.append((score+1, alpha, ana+rest[pos], rest[pos+1:], sofar))
        queue.sort()
        if len(queue) > 10000:
            queue = queue[-10000:]

def show_anagrams(text, max=25, overflow=75):
    """
    Show anagrams of the given text by printing them at the Python command line.
    """
    results = []
    for result, freq in anagram2(text):
        results.sort(key=lambda x: x[1])
        if len(results) < max+overflow-1 or freq >= results[0][1]:
            results.append((result, freq))
            if len(results) > max+overflow:
                results.sort(key=lambda x: x[1])
                print results[-1]
                results = results[1:-1]
    results.reverse()
    for result, freq in results[:max]:
        print (result, freq)
