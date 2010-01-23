# -*- coding: utf-8 -*-

from solvertools.alphabet import *
HAWAIIAN = ALPHABETS['hawaiian']
GREEK = ALPHABETS['greek']

def test_contains():
    assert 'Z' in ENGLISH
    assert 'z' in ENGLISH
    assert '@' not in ENGLISH
    assert '' not in ENGLISH
    assert 'K' in HAWAIIAN
    assert 'T' not in HAWAIIAN
    assert u'\N{GREEK CAPITAL LETTER ALPHA}' in GREEK
    assert u'\N{LATIN CAPITAL LETTER A}' not in GREEK
    assert u'\N{GREEK CAPITAL LETTER ALPHA}' not in ENGLISH
    assert u'α' in GREEK

def test_numbering():
    assert ENGLISH.letter_at(19) == u'S'
    assert HAWAIIAN.letter_at(19) == u'?'
    assert ENGLISH.letter_index('S') == 19
    assert GREEK.letter_index(u'α') == 1

def test_length():
    assert len(ENGLISH) == 26
    assert len(GREEK) == 24

def test_unicode():
    assert isinstance(ENGLISH.letter_at(19), unicode)
    assert isinstance(ENGLISH.letter_at(0), unicode)

