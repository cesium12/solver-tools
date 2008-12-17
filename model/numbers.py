from math import log

def lg(n):
    return log(n) / log(2)

def natnumber_logprob(n):
    assert n >= 0
    expdist = -lg(2)-lg(lg(n))
    if n >= 10: expdist -= 2
    if n > 26: expdist -= 3
    return expdist

