from bayesinator.core import *
from bayesinator.language import english_model
import logging
import math
import solvertools.wordlist as wordlist


logger = logging.getLogger(__name__)


wlist = wordlist.Google200K


substr_freq = {}
total_freq = 0

logger.info("Hashing all substrings in wordlist %s" % wlist.filename)
for word in wlist:
    freq = wlist[word]
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
    s = wlist.convert(s)
    substr = wlist.convert(substr)
    idx = s.find(substr)
    assert idx != -1, "Contract violated: substring not actually contained in superstring."
    if substr in substr_freq and s in wlist:
        return math.log(substr_freq[substr], 2) - math.log(wlist[s], 2)
    return english_model(s[:idx]) + english_model(s[(idx+len(substr)):])
