from solvertools.util import *

def test_load():
    enable = Wordlist('enable.txt')
    enable._load()
    assert 'THE' in enable.words

