from solvertools.regex import bare_regex
from solvertools.wordlist import alphanumeric_only, COMBINED
from solvertools.puzzlebase.mongo import DB, known_word
from solvertools.model.tokenize import tokenize
from math import log, exp
from collections import defaultdict
import re

def associations(words, log_min=-25, beam=1000, multiply=False):
    """
    Find words associated with a set of words in the database. Use a few
    heuristics to find the most relevant results.

    Setting multiply=True makes the results combine multiplicatively,
    essentially saying that the results should be associated with *all* of the
    words. With multiply=False, it adds up the best associations with *any* of
    the words.
    """
    possibilities = set()
    if multiply:
        minimum = log_min
    else:
        minimum = exp(log_min)
    mapping = defaultdict(lambda: defaultdict(lambda: minimum))
    words = [alphanumeric_only(w) for w in words]
    word_freqs = {}
    for word in words:
        word_freqs[word] = COMBINED.get(word, 1000)
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
                    elif not multiply:
                        value = exp(value)
                    mapping[word2][word] = max(mapping[word2][word], value)
    results = {}
    for word2 in possibilities:
        results[word2] = sum([mapping[word2][word]/(word_freqs[word]**.5) for word in words])
        if not multiply:
            # get all results on the same scale
            results[word2] = log(results[word2])
    best_results = sorted(results.items(), key=lambda x: -x[1])
    return best_results

def match_words(words, pattern='.*', n=25, multiply=False):
    if isinstance(pattern, int):
        pattern = '.'*pattern
    if not words:
        return match_pattern(pattern, n)
    re_pattern = re.compile(bare_regex(pattern))
    matches = []
    used = set()
    for word, goodness in associations(words, multiply=multiply):
        match = re_pattern.match(word)
        if match and match.end() == len(word):
            matches.append((word, goodness))
            used.add(word)
            if len(matches) >= n:
                break
    return matches

def match_pattern(pattern, n=25):
    if pattern == '.*':
        raise ValueError("That matches everything.")
    
    matches = COMBINED.grep(pattern)
    matches.sort(key=lambda x: -x[1])
    return matches[:n]

def extract_words(text):
    "Get just the words out of possibly-punctuated text."
    words = tokenize(text).split()
    return [word for word in words if alphanumeric_only(word)]

def match_clue(clue, n=25):
    if clue.strip().endswith('/'):
        clue_text, regex, _ = clue.rsplit('/', 2)
        clue_text = clue_text.strip()
    raise NotImplementedError
