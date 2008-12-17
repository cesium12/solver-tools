from math import log
number_weight = 4        # suppose 1/16 chance that a given token is a number
                         # (that's high, but numbers are important to handle)
def lg(n):
    return log(n) / log(2)

def number_logprob(n):
    if n < 0: return -2+number_logprob(-n)
    expdist = -lg(2)-lg(lg(2+n))
    if n >= 10: expdist -= 2
    if n > 26: expdist -= 5
    return expdist - number_weight

