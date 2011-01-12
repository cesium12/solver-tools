"""
Rearrange text that appears in pieces (such as trigrams in an anaquote) to
form sensible text.
"""
# TODO: possibly extend this to knight's tours and similar, by taking in
# a graph?

from solvertools.model.language_model import split_words
from solvertools.regex import regex_sequence
import logging
logger = logging.getLogger(__name__)

CACHE = {}
def split_words_cached(expr):
    if expr in CACHE:
        return CACHE[expr]
    result = split_words(expr)
    CACHE[expr] = result
    return result

def make_state(pieces):
    scores = [split_words_cached(regex_sequence([piece, '/.*/']))[1]
              for piece in pieces]
    return sum(scores)-len(pieces)*5, tuple(sorted(pieces))

def arrange_pieces(pieces):
    # best-first search
    queue = []
    enqueued = set()
    queue.append(make_state(pieces))
    while queue:
        value, state = queue.pop()
        logger.info((value, state))
        if len(state) == 1:
            return state
        for i in xrange(len(state)):
            for j in xrange(i+1, len(state)):
                the_rest = tuple(state[:i] + state[i+1:j] + state[j+1:])
                val1, state1 = make_state(the_rest + (state[i]+state[j],))
                val2, state2 = make_state(the_rest + (state[j]+state[i],))
                if state1 not in enqueued:
                    queue.append((val1, state1))
                    enqueued.add(state1)
                if state2 not in enqueued:
                    queue.append((val2, state2))
                    enqueued.add(state2)
        queue.sort()

