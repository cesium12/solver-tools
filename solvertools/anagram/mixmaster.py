import numpy as np
from solvertools.anagram.db_lookup import get_anagrams
from solvertools.wordlist import alphagram
from solvertools.anagram.letter_matrix import letters_to_vec, top_pairs, parallel
from solvertools.wordlist import alphanumeric_only, alphanumeric_with_spaces
from solvertools.anagram.permute import swap_distance
from solvertools.util import get_datafile
import heapq, string

matrix = np.load(get_datafile('db/anagram_vectors.npy'))
ranks = np.load(get_datafile('db/anagram_ranks.npy'))

def make_alpha(text):
    return alphagram(alphanumeric_only(text))

def simple_anagram(text):
    """
    Find anagrams that can be made in one cached chunk from the given text.
    """
    alpha = make_alpha(text)
    return list(get_anagrams(alpha))

def multi_anagram(text, num=30):
    alpha = make_alpha(text)
    vec = letters_to_vec(alpha)
    heap = []
    found = 0
    overflow = 0
    used = set()
    first_try = simple_anagram(text)
    used.add(text)
    if first_try:
        found += 1
        first_text, freq = first_try[0]
        score = freq * 10 * differentness(first_text, used)
        if score > 0:
            heapq.heappush(heap, (score, first_text))
            used.add(first_text)
    for value, alpha1, alpha2 in top_pairs(matrix, ranks, vec, num*2):
        for text1, rank1 in get_anagrams(alpha1):
            for text2, rank2 in get_anagrams(alpha2):
                combined_text = text1+' '+text2
                actual_val = parallel(rank1, rank2) * differentness(combined_text, used)
                used.add(combined_text)
                if actual_val > 0:
                    found += 1
                    heapq.heappush(heap, (actual_val, combined_text))
                    if found > num:
                        heapq.heappop(heap)
                        overflow += 1
                # Once we hit overflow, take only one anagram from each pair
                if overflow > num:
                    break
            if overflow > num:
                break
    heap.sort()
    heap.reverse()
    return [(text, val) for (val, text) in heap]

def differentness(text, previous):
    result = min([trigram_goodness(prev, text) for prev in previous])
    return result

def trigram_goodness(original, anagrammed):
    text1 = alphanumeric_only(original)
    text2 = alphanumeric_only(anagrammed)
    trigrams1 = set([text1[i:i+3] for i in xrange(len(text1)-2)])
    trigrams2 = set([text2[i:i+3] for i in xrange(len(text2)-2)])
    return len(trigrams2 - trigrams1) - 2*anagrammed.count(' ')

def swap_goodness(original, anagrammed):
    """
    Calculates how non-trivial an anagram is: it penalizes anagrams that simply
    move entire words around, and rewards those that require many letter swaps
    within or especially between words.
    """
    words1 = alphanumeric_with_spaces(original).split(' ')
    words2 = alphanumeric_with_spaces(anagrammed).split(' ')
    str1 = ''.join(words1)
    str2 = ''.join(words2)
    words1.sort()
    words2.sort()
    str3 = ''.join(words1)
    str4 = ''.join(words2)
    return min(swap_distance(str1, str2), swap_distance(str3, str4))

def wildcard_anagram(text, n=20):
    nblanks = text.count('?')
    if nblanks > 4:
        return [('That has too many blanks.', 0)]
    strings = [text]
    for i in range(nblanks):
        new_strings = [st + c for st in strings for c in string.lowercase]
        strings = new_strings
    got = []
    for anastring in strings:
        simple = simple_anagram(anastring)
        if simple:
            newtext, freq = simple[0]
            got.append((freq, newtext))
    got.sort()
    best = []
    used = set()
    for i in range(1, len(got)+1):
        text = got[-i][1]
        ordered = ' '.join(sorted(text.split()))
        if ordered not in used:
            used.add(ordered)
            best.append(got[-i])
            if len(used) >= n: break
    return best

def anagram(text, num=20):
    if '?' in text:
        return wildcard_anagram(text, num)
    else:
        return multi_anagram(text, num)

def demo():
    print multi_anagram('being john malkovich')
    print multi_anagram('the empire strikes back')

