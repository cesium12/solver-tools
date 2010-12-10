from ply import lex
import re
from solvertools.cipher import lex_base

def dash_to_hyphen(s):
    """
    Replaces various kinds of dash characters with hyphens.
    """
    return re.sub(u'[\u2010\u2011\u2012\u2013\u2014\u2015\u2043\u2212\uff0d]','-',s)

to_morse = {
	'A' : '.-',
	'B' : '-...',
	'C' : '-.-.',
	'D' : '-..',
	'E' : '.',
	'F' : '..-.',
	'G' : '--.',
	'H' : '....',
	'I' : '..',
	'J' : '.---',
	'K' : '-.-',
	'L' : '.-..',
	'M' : '--',
	'N' : '-.',
	'O' : '---',
	'P' : '.--.',
	'Q' : '--.-',
	'R' : '.-.',
	'S' : '...',
	'T' : '-',
	'U' : '..-',
	'V' : '...-',
	'W' : '.--',
	'X' : '-..-',
	'Y' : '-.--',
	'Z' : '--..',
    '0' : '-----',
    '1' : '.----',
    '2' : '..---',
    '3' : '...--',
    '4' : '....-',
    '5' : '.....',
    '6' : '-....',
    '7' : '--...',
    '8' : '---..',
    '9' : '----.',
    '.' : '.-.-.-',
    ',' : '--..--',
    ':' : '---...',
    '?' : '..--..',
    "'" : '.----.',
    '-' : '-....-',
    '/' : '-..-.',
    '(' : '-.--.',
    ')' : '-.--.-',
    '"' : '.-..-.',
    '=' : '-...-',
    '+' : '.-.-.',
    '@' : '.--.-.',
    u'\u00d7' : '-..-'
}

from_morse = lex_base.reverse(to_morse)

class MorseEncoder(lex_base.Encoder):
    
    def __init__(self,**kwargs):
        self.nonalnum = kwargs.get('nonalnum',False)
        super(MorseEncoder,self).__init__(**kwargs)
    
    tokens = (
        'ALNUM',
        'WHITESPACE',
        'KNOWNSYMBOL',
    )

    def t_ALNUM(self,t):
        r'[A-Za-z\d]'
        t.value = to_morse[t.value.upper()]
        return t

    def t_KNOWNSYMBOL(self,t):
        if self.nonalnum:
            t.value = to_morse[t.value]
            return t
        else:
            return None

    t_KNOWNSYMBOL.__doc__ = '[%s]'%re.escape(''.join(filter(lambda x : not x.isalnum(),to_morse.iterkeys())))

class MorseDecoder(lex_base.Decoder):
    tokens = (
        'MORSE',
        'WORDSEP',
    )

    def t_MORSE(self,t):
        r'[.\-]+'
        t.value=from_morse[t.value]
        return t
