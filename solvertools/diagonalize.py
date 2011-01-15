from solvertools.model.language_model import split_words
from itertools import permutations

def diagonalize_all(wordlist):
    results = []
    for permutation in permutations(wordlist):
        try:
            diag = ''.join(permutation[i][i] for i in xrange(len(wordlist)))
        except IndexError:
            continue
        regex = '/'+diag+'/'
        text, goodness = split_words(regex)
        results.append((goodness, regex, text))
    results.sort()
    return results[-100:]
