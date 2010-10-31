# -*- coding: utf-8 -*-
from solvertools import alphabet
from solvertools.model.language_model import getEnglishModel

def caesar_shift(text, offset, alph=alphabet.ENGLISH):
    """
    Performs a Caesar shift by the given offset.

    If the offset is a letter, it will look it up in the alphabet to convert
    it to a shift. (For example, a shift of 'C' means that 'A' goes to 'C',
    which is the same as a shift of 2.)
        
        >>> print caesar_shift('CAESAR', 13)
        PNRFNE
        >>> print caesar_shift(u'ЦАР', 17, alphabet.ALPHABETS['russian'])
        ЖРБ

    """
    if isinstance(offset, basestring):
        try:
            offset = alph.letter_index(offset) - 1
        except KeyError:
            raise ValueError("The offset should either be an integer, or a "
                             "letter of the alphabet.")
    
    shifted = [alph.shift(ch, offset) for ch in text]
    return ''.join(shifted)

def caesar_unshift(text, offset, alph=alphabet.ENGLISH):
    """
    Performs a Caesar shift backwards by the given offset.
    
    If the offset is a letter, it will look it up in the alphabet to convert
    it to a shift. (For example, a shift of 'C' means that 'C' goes to 'A',
    which is the same as a backward shift of 2.)
        
        >>> print caesar_unshift('DBFTBS TIJGU', 1)
        CAESAR SHIFT
    
    """
    if isinstance(offset, basestring):
        try:
            offset = alph.letter_index(offset) - 1
        except KeyError:
            raise ValueError("The offset should either be an integer, or a "
                             "letter of the alphabet.")
    return caesar_shift(text, -offset, alph)

def detect_caesar_shift(text, alph=alphabet.ENGLISH):
    """
    Detects the Caesar shift that turns this text into the most reasonable
    English text. Returns the resulting text, the distance shifted
    (from 0 to 25), and the goodness of the result.

        >>> print detect_caesar_shift('DBFTBS TIJGU')
        (u'CAESAR SHIFT', 25, -2.7035009155418437)
        >>> print detect_caesar_shift('HAL')
        (u'IBM', 1, -4.6171190236825206)

    """
    theModel = getEnglishModel()
    N = len(alph)
    results = []
    for shift in xrange(N):
        answer = caesar_shift(text, shift)
        results.append((answer, shift, theModel.text_goodness(answer)))
    results.sort(key=lambda x: -x[2])
    return results[0]
    
