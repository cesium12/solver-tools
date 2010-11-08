import bayesinator.alphabet as alphabet
from bayesinator.core import *
import logging
import math
import solvertools.model.language_model as model
import solvertools.wordlist as wordlist


logger = logging.getLogger(__name__)


@puzzle_property(basestring)
def word(s):
    return s in wordlist.COMBINED


@entropy_function(alphabet.english)
def english_model(s):
    return -model.get_english_model().text_logprob(s)


substr_freq = {}
total_freq = 0
substr_wordlist = wordlist.Google200K
logger.info("Hashing all substrings in wordlist %s" % substr_wordlist.filename)
for word in substr_wordlist:
    freq = substr_wordlist[word]
    total_freq += freq
    n = len(word)
    for i in range(n):
        for j in range(i+1, n+1):
            substr = word[i:j]
            if substr in substr_freq:
                substr_freq[substr] += freq
            else:
                substr_freq[substr] = freq
logger.info("Done hashing substrings")


def superstring_entropy(s, substr):
    """
    Returns the amount of information contained in a string given that
    it contains a particular string as a substring.
    """
    if substr in substr_freq:
        return math.log(substr_freq[substr], 2)
    idx = s.find(substr)
    assert idx != -1, "Contract violated: substring not actually contained in superstring."
    return english_model(s[:idx]) + english_model(s[(idx+len(substr)):])
