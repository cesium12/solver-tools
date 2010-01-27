# -*- coding: utf-8 -*-
"""
This module is meant for dealing with "Arpabet" phonetic spelling, particularly
converting it to approximate IPA so you don't have to understand its
frustratingly misleading vowels.

This uses only a subset of the IPA vowels that appear in English, and in
doing so, eliminates many dialect distinctions. IPA /ɑ/ is represented as the
plain old Roman letter "a", as some fonts don't even distinguish these and
the Arpabet definitely doesn't.

Vowel length is not represented.

Use rough_ipa() if you want an even rougher version.
"""

ARPA_TO_IPA = {
    u'AO': u'ɔ',
    u'AA': u'a',
    u'IY': u'i',
    u'UW': u'u',
    u'EH': u'ɛ',
    u'IH': u'ɪ',
    u'UH': u'ʊ',
    u'AH': u'ə',
    u'AE': u'æ',

    u'EY': u'eɪ',
    u'AY': u'aɪ',
    u'OW': u'oʊ',
    u'AW': u'aʊ',
    u'OY': u'ɔɪ',

    u'ER': u'ɝ',
    u'P': u'p',
    u'B': u'b',
    u'T': u't',
    u'D': u'd',
    u'K': u'k',
    u'G': u'g',
    u'M': u'm',
    u'N': u'n',
    u'NG': u'ŋ',
    
    u'F': u'f',
    u'V': u'v',
    u'TH': u'θ',
    u'DH': u'ð',
    u'S': u's',
    u'Z': u'z',
    u'SH': u'ʃ',
    u'ZH': u'ʒ',
    u'HH': u'h',
    u'L': u'l',
    u'R': u'r',
    u'Y': u'j',
    u'W': u'w',
    u'CH': u'tʃ',
    u'JH': u'dʒ',
}

ROUGH_IPA_VOWELS = {
    u'ɔ': u'o',
    u'ɛ': u'e',
    u'ʊ': u'u',
    u'æ': u'a',
    u'ɝ': u'ər'
}

IPA_VOWELS = u'uʊoɔaæəeɝɪi'
def rough_ipa(ipa):
    out = []
    last = ''
    for char in ipa:
        # people can't tell the difference between ɪ and i after a vowel
        if char == 'ɪ' and last in IPA_VOWELS:
            out.append('i')
        elif char in ROUGH_IPA_VOWELS:
            out.append(ROUGH_IPA_VOWELS[char])
        else:
            out.append(char)
