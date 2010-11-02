from bayesinator.core import *
from solvertools.alphabet import ALPHABETS



@puzzle_property(basestring)
def english(s):
    return all (c in ALPHABETS['english'] for c in ''.join(s.split()))

@puzzle_property(basestring)
def english_mit(s):
    return all (c in ALPHABETS['english_mit'] for c in ''.join(s.split()))

@puzzle_property(basestring)
def english_playfair(s):
    return all (c in ALPHABETS['english_playfair'] for c in ''.join(s.split()))

@puzzle_property(basestring)
def spanish(s):
    return all (c in ALPHABETS['spanish'] for c in ''.join(s.split()))

@puzzle_property(basestring)
def spanish_old(s):
    return all (c in ALPHABETS['spanish_old'] for c in ''.join(s.split()))

@puzzle_property(basestring)
def hawaiian(s):
    return all (c in ALPHABETS['hawaiian'] for c in ''.join(s.split()))

@puzzle_property(basestring)
def swedish(s):
    return all (c in ALPHABETS['swedish'] for c in ''.join(s.split()))

@puzzle_property(basestring)
def norwegian(s):
    return all (c in ALPHABETS['norwegian'] for c in ''.join(s.split()))

@puzzle_property(basestring)
def greek(s):
    return all (c in ALPHABETS['greek'] for c in ''.join(s.split()))

@puzzle_property(basestring)
def greek_ascii(s):
    return all (c in ALPHABETS['greek_ascii'] for c in ''.join(s.split()))

@puzzle_property(basestring)
def russian(s):
    return all (c in ALPHABETS['russian'] for c in ''.join(s.split()))

@puzzle_property(basestring)
def digits(s):
    return all (c in ALPHABETS['digits'] for c in ''.join(s.split()))

@puzzle_property(basestring)
def hex(s):
    return all (c in ALPHABETS['hex'] for c in ''.join(s.split()))

@puzzle_property(basestring)
def base64(s):
    return all (c in ALPHABETS['base64'] for c in ''.join(s.split()))
