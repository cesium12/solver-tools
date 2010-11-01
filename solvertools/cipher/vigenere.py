# -*- coding: utf-8 -*-
from solvertools import alphabet
from solvertools.cipher.caesar import caesar_shift, caesar_unshift
import itertools

"""
Implements the polyalphabetic Vigenère cipher (Vigenère's weaker but more
well-known cipher).
"""

def vigenere_encipher(plaintext, key, alph=alphabet.ENGLISH):
    """
    Enciphers text using a Vigenère cipher.

        >>> print vigenere_encipher('attack at dawn', 'melon')
        MXEOPW EE RNIR
    """
    cycle = itertools.cycle(key)
    out = []
    for ch in plaintext:
        if ch not in alph:
            out.append(ch)
        else:
            enciphered = caesar_shift(ch, cycle.next())
            out.append(enciphered)
    return ''.join(out)

def vigenere_decipher(plaintext, key, alph=alphabet.ENGLISH):
    """
    Deciphers text using a Vigenère cipher.
        
        >>> print vigenere_decipher('MXEOPW EE RNIR', 'melon')
        ATTACK AT DAWN
    """
    cycle = itertools.cycle(key)
    out = []
    for ch in plaintext:
        if ch not in alph:
            out.append(ch)
        else:
            enciphered = caesar_unshift(ch, cycle.next())
            out.append(enciphered)
    return ''.join(out)


