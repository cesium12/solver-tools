# -*- coding: utf-8 -*-
"""
This module is meant for dealing with "Arpabet" phonetic spelling, particularly
converting it to approximate IPA so you don't have to understand the Arpabet's
frustratingly misleading vowels.

This uses only a subset of the IPA vowels that appear in English, and in doing
so, eliminates many dialect distinctions. IPA [ɑ] and similar vowels are all
represented as the plain old Roman letter "a", for example.

Other simplifications: Vowel length is not represented. r's are separated from
the vowels (sorry, Brits) and written right-side-up (sorry, linguists). A few
different central vowels are all represented as "ə" (even though only the
unaccented ones can actually be schwas).

This actually does not lose much information given Arpabet input. Most similar
vowels are already smashed together anyway.

The nine monophthong vowels in this representation are (following a sort of continuum):

    u ʊ o ə a æ e ɪ i

When the input contains stress notation, primary stress is indicated with an
apostrophe before the vowel.
"""
import string

IPA_VOWELS = u'uʊoaæəeɪi'

ARPA_TO_IPA = {
   'AA': u'a',
   'AE': u'æ',
   'AH': u'ə',
   'AW': u'aʊ',
   'AY': u'aɪ',
   'EH': u'e',
   'ER': u'ər',
   'EY': u'eɪ',
   'IH': u'ɪ',
   'IY': u'i',
   'AO': u'o',
   'OW': u'oʊ',
   'OY': u'oɪ',
   'UH': u'ʊ',
   'UW': u'u',
   'W': u'w',
   'Y': u'j',
   
   'B': u'b',
   'CH': u'tʃ',
   'D': u'd',
   'DH': u'ð',
   'F': u'f',
   'G': u'g',
   'HH': u'h',
   'JH': u'dʒ',
   'K': u'k',
   'L': u'l',
   'M': u'm',
   'N': u'n',
   'NG': u'ŋ',
   'P': u'p',
   'R': u'r',
   'S': u's',
   'SH': u'ʃ',
   'T': u't',
   'TH': u'θ',
   'V': u'v',
   'Z': u'z',
   'ZH': u'ʒ',
}

def arpa_symbol_to_ipa(s):
    """
    Convert an individual phonetic symbol from ARPA to IPA.
    """
    if s[-1] in string.digits:
        phon = ARPA_TO_IPA[s[:-1]]
        if s[-1] == '1':
            return u"'" + phon
        else:
            return phon
    else:
        return ARPA_TO_IPA[s]

def arpa_to_ipa(s):
    """
    Given a word spelled phonetically in the Arpabet, convert it to approximate
    IPA.

        >>> print arpa_to_ipa('S EY1 JH IH0 Z')
        s'eɪdʒɪz
    """
    phonemes = s.split()
    return u''.join(arpa_symbol_to_ipa(phon) for phon in phonemes)

