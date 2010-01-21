# -*- coding: utf-8 -*-
from solvertools.wordlist import *

def test_load():
    assert 'THE' in ENABLE
    assert 'the' in ENABLE
    assert 'zyzzlvaria' not in ENABLE
    assert u'zürich' in NPL

