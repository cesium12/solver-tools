"""
A last-minute feature request. Determines if letters follow certain
distributions. Feel free to define your own, too.
"""

from solvertools.alphabet import ENGLISH
from solvertools.puzzle_array import PuzzleArray, Header
import numpy as np

ENGLISH_UNIGRAMS = np.array([.08167, .01492, .02782, .04253, .12702, .02228,
.02015, .06094, .06966, .00153, .00772, .04025, .02406, .06749, .07507, .01929,
.00095, .05987, .06327, .09056, .02758, .00978, .02360, .00150, .01974, .00074
])

def distribution_distance(dist1, dist2):
    """
    How different are these two probability distributions?
    """
    return np.sum(np.power(dist1 - dist2, 2))

def distribution_distance_sorted(dist1, dist2):
    """
    How likely is it that dist1 was sampled from some *permutation* of dist2,
    normalized from 0 to 1?
    """
    sorted1 = np.sort(dist1)
    sorted2 = np.sort(dist2)
    return np.sum(np.power(sorted1 - sorted2, 2)) * 2  # this is a totally made up prior

def letter_distribution(text, alphabet=ENGLISH):
    """
    Make a frequency distribution out of text.
    """
    text = alphabet.normalize(text)
    counts = np.array([text.count(letter) for letter in alphabet], 'f')
    total = np.sum(counts)
    if total == 0:
        total = 1
    return counts / total

def uniform_distribution(n=26):
    return np.ones((n,)) / n

def evaluate_letter_distribution(text):
    """
    Prints out how well the letter frequencies in `text` compares to various
    known letter distributions. For now, those are:

    - Uniformly random
    - English
    - Cryptograms of English

    It gives a "badness" value for each, so the best distribution is the one
    with the lowest badness.
    """
    dist = letter_distribution(text)
    eval_uniform = distribution_distance(dist, uniform_distribution())
    eval_english = distribution_distance(dist, ENGLISH_UNIGRAMS)
    eval_crypto = distribution_distance_sorted(dist, ENGLISH_UNIGRAMS)
    results = PuzzleArray([
        [Header("Distribution"), Header("Badness")],
        ["Uniformly random", eval_uniform],
        ["English letter frequencies", eval_english],
        ["Cryptogram of English", eval_crypto]
    ])
    results = results.sort_by(1)
    print results
    return results
