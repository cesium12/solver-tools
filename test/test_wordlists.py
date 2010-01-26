# -*- coding: utf-8 -*-
from solvertools.wordlist import *

TestWords = Wordlist('testwords', case_insensitive, with_frequency,
pickle=False)

def test_wordlists():
    assert 'THE' in TestWords
    assert 'the' in TestWords
    assert 'zyzzlvaria' not in TestWords

def test_variants():
    assert u'zürich' in TestWords
    assert u'zürich' in TestWords.variant(alphanumeric_only)
    assert u'zurich' in TestWords.variant(alphanumeric_only)
    assert u'zurich' in TestWords.variant(asciify)
    assert u'ZURICH' not in TestWords.variant(asciify)

def test_order():
    iterator = iter(TestWords)
    assert iterator.next() == 'THE'
