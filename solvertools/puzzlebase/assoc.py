from solvertools.wordlist import alphanumeric_only, Google1M
from solvertools.puzzlebase.mongo import DB, known_word
from math import log, exp
from collections import defaultdict

def associations(words, log_min=-25, beam=1000, logscale=True):
    possibilities = set()
    if logscale:
        minimum = log_min
    else:
        minimum = exp(log_min)
    mapping = defaultdict(lambda: defaultdict(lambda: minimum))
    words = [alphanumeric_only(w) for w in words]
    word_freqs = {}
    for word in words:
        word_freqs[word] = Google1M.get(word, 1000)
        query = DB.relations.find({'words': word})
        for match in query[:beam]:
            for word2 in match['words']:
                if word2 not in words:
                    possibilities.add(word2)
                    value = match.get('interestingness')
                    if value is None:
                        # interestingness hasn't yet been set on this
                        # relation, so guess
                        value = minimum/2
                    elif not logscale:
                        assert exp(value) < 1
                        value = exp(value)
                    mapping[word2][word] = max(mapping[word2][word], value)
    results = {}
    for word2 in possibilities:
        results[word2] = sum([mapping[word2][word]/log(word_freqs[word]) for word in words])
    best_results = sorted(results.items(), key=lambda x: -x[1])
    return best_results
