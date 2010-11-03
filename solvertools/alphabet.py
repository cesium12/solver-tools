# -*- coding: utf-8 -*-
"""
You never know what alphabet you'll end up trying to solve a cryptogram in.

If, like most alphabets implemented here, the alphabet has a concept of
uppercase and lowercase versions of a letter, use a CaseAlphabet, and give only
the uppercase ones to the constructor.

Alphabets can be indexed in both directions. Keep in mind that all indices are
1-based, following puzzle traditions while breaking Python traditions.

Feel free to add more alphabets.
"""

from solvertools.lib.ordered_set import OrderedSet
import string

class Alphabet(OrderedSet):
    """
    The base class of alphabets. Implements the bi-directional, 1-based index,
    and that's about it.
    """
    def __init__(self, letters):
        OrderedSet.__init__(self, [self.normalize(c) for c in letters])

    def normalize(self, char):
        """
        Don't do anything to the inputs by default.
        
        This enables the default Alphabet class to be used for any hashable
        object, not just strings, if a reason to do so arises.
        """
        return char

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
        """
        The basic operation of a Caesar shift. Shifts the given letter forward
        in the alphabet by `offset`, or backward if it is negative.

        Use `letter_shift` if you want to instead specify, for example, what
        the letter A maps to.
        """
        if letter not in self:
            return letter
        return self[(self.index(self.normalize(letter)) + offset) % len(self)]
    
    def letter_difference(self, letter1, letter2):
        """
        Returns the distance in the alphabet that `letter2` comes after
        `letter1`, wrapping around if necessary. Conceptually, it's
        `letter2 - letter1`.
        """
        if letter1 not in self:
            raise IndexError("%s is not a letter" % letter1)
        if letter2 not in self:
            raise IndexError("%s is not a letter" % letter2)
        return (self.index(letter2) - self.index(letter1)) % len(self)
    
    def letter_shift(self, letter, sourceletter, targetletter):
        """
        If `sourceletter` shifts to `targetletter`, what does `letter` shift to?
        """
        if sourceletter is None: sourceletter = self.letter_at(1)
        return self.shift(letter, self.letter_difference(sourceletter, targetletter))

    def text_to_indices(self, text):
        """
        Represent text as a sequence of letter indices.
        """
        return [self.letter_index(char) for char in text if char in self]
    letters_to_indices = text_to_indices

    def indices_to_letters(self, indices):
        """
        Turn a sequence of letter indices into a sequence of letters.
        """
        return [self.letter_at(i) for i in indices]

    def indices_to_text(self, indices):
        """
        Turn a sequence of letter indices into a string from the alphabet.
        """
        return ''.join([self.letter_at(i) for i in indices])

    def sort(self, texts):
        """
        Sort a list according to the ordering of a particular alphabet.
        """
        return sorted(texts, key=self.text_to_indices)

    def __repr__(self):
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        return u"%s(%r)" % (self.__class__.__name__, self.items)

class TextAlphabet(Alphabet):
    """
    An alphabet whose symbols are Unicode strings (which is all of them so far).
    """
    def __init__(self, letters):
        Alphabet.__init__(self, letters)
        self.max_width = max(len(letter) for letter in self.items)

    def normalize(self, char):
        """
        Just make sure everything is Unicode.
        """
        return unicode(char)

    def __unicode__(self):
        if self.max_width == 1:
            return u'%s(u"%s")' % (self.__class__.__name__,
                                   u''.join(self.items))
        else:
            return Alphabet.__unicode__(self)

class CaseAlphabet(TextAlphabet):
    """
    Use this class for alphabets that have an upper/lowercase distinction that
    we want to ignore. This is the case for most European-derived alphabets.
    
    This requires that string.upper() does the right thing.
    """
    def shift(self, letter, offset):
        "The basic operation of a Caesar shift. The math here is 0-based."
        if letter not in self: return letter
        output = self[(self.index(self.normalize(letter)) + offset) % len(self)]
        if letter == letter.lower():
            output = output.lower()
        return output
    def normalize(self, char):
        """
        When comparing letters in the alphabet, we want to ensure that
        they are Unicode characters, and capitalized if possible.
        """
        return unicode(char).upper()

ALPHABETS = {
  ### Latin-derived alphabets ###

  # our favorite, 26-letter alphabet
  'english': CaseAlphabet(string.uppercase),
  
  # 25-letter variants of the alphabet
  'english_mit': CaseAlphabet(u"ABCDEFGHIJKLMNOPQRSTVWXYZ"),
  'english_playfair': CaseAlphabet(u"ABCDEFGHIKLMNOPQRSTUVWXYZ"),

  # Latin (23 letters, I=J, U=V, no W)
  'latin': CaseAlphabet(u"ABCDEFGHIKLMNOPQRSTVXYZ"),
  
  # Modern Spanish alphabet (27 letters, standardized in 1994)
  'spanish': CaseAlphabet(u"ABCDEFGHIJKLMNÑOPQRSTUVWXYZ"),

  # Obsolete Spanish alphabet (pre-1994)
  # (29 letters including digraphs; RR is not considered a letter, however)
  'spanish_old': CaseAlphabet(['A', 'B', 'C', 'CH', 'D', 'E', 'F', 'G', 'H',
                               'I', 'J', 'K', 'L', 'LL', 'M', 'N', u'Ñ', 'O',
                               'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X',
                               'Y', 'Z']),

  # The 12-letter Hawaiian alphabet
  # (disregarding the okina, because everybody does)
  'hawaiian': CaseAlphabet(u"AEIOUHKLMNPW"),
  
  # The 29-letter Swedish alphabet
  'swedish': CaseAlphabet(unicode(string.uppercase)+u'ÅÄÖ'),

  # The 29-letter Norwegian alphabet (which is also the Danish alphabet)
  'norwegian': CaseAlphabet(unicode(string.uppercase)+u'ÆØÅ'),

  # Turkish is hard to do right, skipping it for now.

  ### Non-Latin alphabets ###

  # The 24-letter Greek alphabet, written in two ways:
  # With Greek Unicode characters that often look deceptively like Latin ones
  'greek': CaseAlphabet(u"ΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩ"),

  # Or, as Latinized in the Microsoft Symbol font
  'greek_ascii': CaseAlphabet(u"ABGDEZHQIKLMNXOPRSTUFCYW"),

  ### Cyrillic alphabets ###
  # The 33-letter Russian alphabet
  'russian': CaseAlphabet(u"АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"),
  
  # The 33-letter Ukrainian alphabet
  'ukrainian': CaseAlphabet(u"АБВГҐДЕЄЖЗИІЇЙКЛМНОПРСТУФХЦЧШЩЬЮЯ"),

  ### Computational 'alphabets' ###
  'digits': TextAlphabet(string.digits),
  'hex': CaseAlphabet(string.digits + "ABCDEF"),
  'base64': TextAlphabet(string.uppercase + string.lowercase
                         + string.digits + "+/")
}

ENGLISH = ALPHABETS['english']

def demo():
    "Demo: Show all defined alphabets."
    for key, value in ALPHABETS.items():
        print "%s: %s" % (key, value)

if __name__ == '__main__':
    demo()
# vim:tw=0:
