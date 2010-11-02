import bayesinator.alphabet as alphabet
from solvertools.cipher.caesar import caesar_shift
from bayesinator.core import *
import math


@transformation(alphabet.english)
def rot13(s):
    t = []
    for c in s:
        if 'a' <= c <= 'z':
            t.append(chr(ord('a') + ((ord(c) - ord('a') + 13) % 26)))
        elif 'A' <= c <= 'Z':
            t.append(chr(ord('A') + ((ord(c) - ord('A') + 13) % 26)))
        else:
            t.append(c)
    yield ''.join(t)


def gen_caesar_shift(alphaname):
    def caesar(text):
        alpha = alphabet.ALPHABETS[alphaname]
        n = alpha.size()
        entropy = math.log(n,2)
        for offset in range(1,n):
            yield Transform(caesar_shift(text, offset, alpha), entropy, offset)
    caesar.__name__ = 'caesar_shift_' + alphaname
    return caesar

transformation(alphabet.english)(gen_caesar_shift('english'))
transformation(alphabet.english_mit)(gen_caesar_shift('english_mit'))
transformation(alphabet.english_playfair)(gen_caesar_shift('english_playfair'))
transformation(alphabet.spanish)(gen_caesar_shift('spanish'))
transformation(alphabet.spanish_old)(gen_caesar_shift('spanish_old'))
transformation(alphabet.hawaiian)(gen_caesar_shift('hawaiian'))
transformation(alphabet.swedish)(gen_caesar_shift('swedish'))
transformation(alphabet.norwegian)(gen_caesar_shift('norwegian'))
transformation(alphabet.greek)(gen_caesar_shift('greek'))
transformation(alphabet.greek_ascii)(gen_caesar_shift('greek_ascii'))
transformation(alphabet.russian)(gen_caesar_shift('russian'))
#transformation(alphabet.digits)(gen_caesar_shift('digits'))
#transformation(alphabet.hex)(gen_caesar_shift('hex'))
transformation(alphabet.base64)(gen_caesar_shift('base64'))
