from math import log

def lg(n):
    return log(n) / log(2)

def number_logprob(n):
    if n < 0: return -2+number_logprob(-n)
    expdist = -lg(2)-lg(lg(2+n))
    if n >= 10: expdist -= 2
    if n > 26: expdist -= 3
    return expdist

