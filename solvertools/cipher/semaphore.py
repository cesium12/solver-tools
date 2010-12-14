# -*- coding: utf-8 -*-
"""
Encoder and decoder for semaphore.  For ease of entry, directions
are represented by the corresponding numeric keypad numbers i. e.
1 = SW, 2 = S, 3 = SE, 4 = W etc.
"""

from solvertools.cipher import lex_base
from ply import lex
import string

to_sem = {
    'A' : '12',
    'B' : '42', 
	'C' : '72',
	'D' : '82',
	'E' : '92',
	'F' : '62',
	'G' : '32',
	'H' : '41',
	'I' : '71',
	'J' : '68',
	'K' : '18',
	'L' : '19',
	'M' : '61',
	'N' : '13',
	'O' : '74',
	'P' : '84',
	'Q' : '94',
	'R' : '46',
	'S' : '43',
	'T' : '78',
	'U' : '79',
	'V' : '83',
	'W' : '96',
	'X' : '93',
	'Y' : '76',
	'Z' : '63',
    '#' : '89',
}

from_sem = lex_base.reverse(to_sem)
#semaphore is unordered
for (k,v) in from_sem.items():
    from_sem[k[1]+k[0]]=v

class InputMode(object):

    numpad_chars = '12346789'
    numpad_ords = map(ord,numpad_chars)

    def to_numpad(self,x):
        raise NotImplemented

    def from_numpad(self,x):
        raise NotImplemented

class TranslateInput(InputMode):

    def __init__(self,chars):
        ords = map(ord,chars)
        self.to_trans = dict(zip(ords, InputMode.numpad_ords))
        self.from_trans = dict(zip(InputMode.numpad_ords, ords))

    def to_numpad(self,x):
        return unicode(x).translate(self.to_trans)

    def from_numpad(self,x):
        return unicode(x).translate(self.from_trans)

NUMPAD = TranslateInput(InputMode.numpad_chars)
PHONEPAD = TranslateInput('78946123')
VI = TranslateInput('bjnhlyku')
ARROW = TranslateInput(u'↙↓↘←→↖↑↗')

class SemaphoreEncoder(lex_base.Encoder):

    states = (
        ('num','exclusive'),
    )

    tokens = (
        'ALNUM',
        'WHITESPACE',
        'CHANGEMODE',
    )
   
    def __init__(self,**kwargs):
        self.input_mode = kwargs.pop('input_mode',NUMPAD)
        super(SemaphoreEncoder,self).__init__(**kwargs)

    def __call__(self,s):
        return self.input_mode.from_numpad(super(SemaphoreEncoder,self).__call__(s))

    def t_ALNUM(self,t):
        r'[A-Za-z]'
        t.value = to_sem[t.value.upper()]
        return t

    def t_num_ALNUM(self,t):
        r'\d'
        if t.value == '0':
            t.value = to_sem['K']
        else:
            t.value = to_sem[chr(ord(t.value)-ord('1')+ord('A'))]
        return t

    def t_CHANGEMODE(self,t):
        r'(?=\d)'
        t.value=to_sem['#']
        t.lexer.begin('num')
        return t

    def t_num_CHANGEMODE(self,t):
        r'(?=\D)'
        t.value=to_sem['J']
        t.lexer.begin('INITIAL')
        return t

class SemaphoreDecoder(lex_base.Decoder):
    states = (
        ('num', 'exclusive'),
    )

    tokens = (
        'SEMAPHORE',
        'WORDSEP',
        'CHMODE',
    )

    def __init__(self,**kwargs):
        self.input_mode = kwargs.pop('input_mode',NUMPAD)
        super(SemaphoreDecoder,self).__init__(**kwargs)

    def __call__(self,s):
        return super(SemaphoreDecoder,self).__call__(self.input_mode.to_numpad(s))
   
    def t_SEMAPHORE(self,t):
        r'[1-46-9]{2}'
        t.value=from_sem[t.value]
        if t.value=='#':
            t.lexer.begin('num')
            return None
        else:
            return t

    def t_num_SEMAPHORE(self,t):
        r'[1-46-9]{2}'
        tmp = from_sem[t.value]
        if tmp=='J':
            t.lexer.begin('INITIAL')
            return None
        elif tmp=='K':
            t.value = '0'
        else:
            t.value = chr(ord(tmp)-ord('A')+ord('1'))
        return t

    def t_CHMODE(self,t):
        r'89|98'
        t.lexer.begin('num')
        return None

    def t_num_CHMODE(self,t):
        r'68|86'
        t.lexer.begin('INITIAL')
        return None
