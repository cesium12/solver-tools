# -*- coding: utf-8 -*-
"""
This module implements a one-to-one mapping between approximate IPA and the
Roman alphabet plus six characters.

This allows Regulus to work with IPA without having to understand Unicode, or
really without having to understand anything beyond "subtract 65 from the
character code". As a bonus, it is easier to type if you happen to know the
mapping.

Spaces are preserved, though they're presumably discarded later. On the Roman
side, capitalization doesn't matter (the output is all caps). On the IPA side,
all characters must be lowercase.
    
For example, here is how to convert the representation of the phrase
"English speech" between IPA and this character set:

    >>> print ipa_to_roman(u"'ɪŋglɪʃ sp'itʃ")
    `YQGLYX SP`ITX
    >>> print roman_to_ipa("`Yqglyx sp`itx")
    'ɪŋglɪʃ sp'itʃ

In Roman-ish IPA, the first sentence of this documentation is:

    ]`YS M`ADCUL `YMPL_MENTS _ W`_N TU W`_N M`^PYQ BITW`IN _PR`AKSYM_T
    `AY P`I `EY ^ND ]_ R`O\\M_N `ELF_BET PL`_S S`YX K`^RYKT_RZ

"""

IPA_TO_ROMAN = {
    u'a': 'A',
    u'b': 'B',
    u'ʒ': 'C',
    u'd': 'D',
    u'e': 'E',
    u'f': 'F',
    u'g': 'G',
    u'h': 'H',
    u'i': 'I',
    u'j': 'J',
    u'k': 'K',
    u'l': 'L',
    u'm': 'M',
    u'n': 'N',
    u'o': 'O',
    u'p': 'P',
    u'ŋ': 'Q',
    u'r': 'R',
    u's': 'S',
    u't': 'T',
    u'u': 'U',
    u'v': 'V',
    u'w': 'W',
    u'ʃ': 'X',
    u'ɪ': 'Y',
    u'z': 'Z',
    u'θ': '[',
    u'ʊ': '\\',
    u'ð': ']',
    u'ə': '_',
    u'æ': '^',
    u"'": "`",
    u' ': ' ',
}

ROMAN_TO_IPA = {}
for key, val in IPA_TO_ROMAN.items():
    ROMAN_TO_IPA[val] = key

def ipa_to_roman(word):
    """
    Convert a word in rough IPA to the Roman-ish character set.
    """
    return ''.join(IPA_TO_ROMAN[ch] for ch in word)

def roman_to_ipa(word):
    """
    Convert a word in the Roman-ish character set to rough IPA.
    """
    return ''.join(ROMAN_TO_IPA[ch] for ch in word.upper())
