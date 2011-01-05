from solvertools.wordlist import alphanumeric_only
from solvertools.puzzlebase.mongo import DB
from math import log, exp
from collections import defaultdict

def associations(words, n=10, beam=50, log_min=-20, logscale=False):
    possibilities = set()
    if logscale:
        minimum = log_min
    else:
        minimum = exp(log_min)
    mapping = defaultdict(lambda: defaultdict(lambda: minimum))
    words = [alphanumeric_only(w) for w in words]
    for word in words:
        query = DB.relations.find({'words': word})
        for match in query[:beam]:
            for word2 in match['words']:
                if word != word2 and word2 not in possibilities:
                    possibilities.add(word2)
                    value = match.get('interestingness')
                    if value is None:
                        # interestingness hasn't yet been set on this
                        # relation, so guess
                        value = minimum/2
                    if not logscale:
                        value = exp(value)
                    mapping[word2][word] = max(mapping[word2][word], value)

    results = {}
    for word2 in possibilities:
        results[word2] = sum([mapping[word2][word] for word in words])
    best_results = sorted(results.items(), key=lambda x: -x[1])
    return best_results[:n]
