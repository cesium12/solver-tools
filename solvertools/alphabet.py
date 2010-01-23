# -*- coding: utf-8 -*-
"""
You never know what alphabet you'll end up trying to solve a cryptogram in.

If the alphabet has a concept of uppercase and lowercase versions of a letter,
use only the uppercase ones. Feel free to add more alphabets.
"""

from solvertools.lib.ordered_set import OrderedSet
import string
import numpy

class Alphabet(OrderedSet):
    def __init__(self, letters):
        OrderedSet.__init__(self, [self.normalize(c) for c in letters])
    def normalize(self, char):
        """
        When comparing letters in the alphabet, we want to ensure that
        they are Unicode characters, and capitalized if possible.
        """
        return unicode(char).upper()
    def __contains__(self, char):
        return self.indices.__contains__(self.normalize(char))
    def letter_index(self, char):
        """
        Implements A=1, B=2, C=3, etc.

        If the given letter is in this alphabet, return its 1-based position
        in the alphabet. Otherwise, return 0.
        """
        if char in self:
            return self.index(self.normalize(char))+1
        else: return 0
    def letter_at(self, index):
        """
        Returns the letter at the given 1-based position. Returns '?' for
        an index outside the range of the alphabet.
        """
        if (index >= 1) and (index <= len(self)):
            return self[index-1]
        else:
            return u'?'
    def shift(self, letter, offset):
        "The basic operation of a Caesar shift. The math here is 0-based."
        if letter not in self: return letter
        return self[(self.index(letter) + offset) % len(self)]

ALPHABETS = {
  ### Latin-derived alphabets ###

  # our favorite, 26-letter alphabet
  'english': Alphabet(string.uppercase),
  
  # 25-letter variants of the alphabet
  'english_mit': Alphabet(u"ABCDEFGHIJKLMNOPQRSTVWXYZ"),
  'english_playfair': Alphabet(u"ABCDEFGHIKLMNOPQRSTUVWXYZ"),
  
  # Modern Spanish alphabet (27 letters, standardized in 1994)
  'spanish': Alphabet(u"ABCDEFGHIJKLMNÑOPQRSTUVWXYZ"),

  # Obsolete Spanish alphabet (pre-1994)
  # (29 letters including digraphs; RR is not considered a letter, however)
  'spanish_old': Alphabet(['A', 'B', 'C', 'CH', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'LL', 'M', 'N', u'Ñ', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']),

  # The 12-letter Hawaiian alphabet
  # (disregarding the okina, because everybody does)
  'hawaiian': Alphabet(u"AEIOUHKLMNPW"),
  
  # The 29-letter Swedish alphabet
  'swedish': Alphabet(unicode(string.uppercase)+u'ÅÄÖ'),

  # The 29-letter Norwegian alphabet (which is also the Danish alphabet)
  'norwegian': Alphabet(unicode(string.uppercase)+u'ÆØÅ'),

  # The 29-letter Turkish alphabet
  # (WARNING: str.upper() and str.lower() do not work for Turkish! They'll put
  # the dots on the wrong i's.)
  'turkish': Alphabet(u"ABCÇDEFGĞHIİJKLMNOÖPRSŞTUÜVYZ"),

  ### Non-Latin alphabets ###

  # The 24-letter Greek alphabet, written in two ways:
  # With Greek Unicode characters that often look deceptively like Latin ones
  'greek': Alphabet(u"ΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩ"),

  # Or, as Latinized in the Microsoft Symbol font
  'greek_ascii': Alphabet(u"ABGDEZHQIKLMNXOPRSTUFCYW"),

  ### Cyrillic alphabets ###
  # The 33-letter Russian alphabet
  'russian': Alphabet(u"АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"),
  
  # The 33-letter Ukrainian alphabet
  'ukrainian': Alphabet(u"АБВГҐДЕЄЖЗИІЇЙКЛМНОПРСТУФХЦЧШЩЬЮЯ"),
}

ENGLISH = ALPHABETS['english']
# vim:tw=0:
