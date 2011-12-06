# -*- coding: utf-8 -*-
"""
Encoder and decoder for semaphore.  There are several different modes
of inputing semaphore directions: keypad (1=SW, 2=S etc.), phonepad
(1=NW, 2=N, etc.), vi (h=W, j=S, etc.), and unicode arrows (U+2190=W,
U+2191=N, etc.).
"""

from solvertools.cipher import lex_base
from ply import lex
import string

to_semaphore = {
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

from_semaphore = lex_base.reverse_dict(to_semaphore)
#semaphore is unordered
for (k,v) in from_semaphore.items():
    from_semaphore[k[1]+k[0]]=v

class SemaphoreInputMode(object):
    '''
    Each SemaphoreInputMode instance defines a way of representing
    semaphore as a string of unicode characters.
    '''

    numpad_chars = '12346789'
    numpad_ords = map(ord,numpad_chars)

    def to_numpad(self,x): 
        raise NotImplemented

    def from_numpad(self,x):
        raise NotImplemented

class SemaphoreTranslateInput(SemaphoreInputMode):
    '''
    A SemaphoreInputMode in which each semaphore arrow is represented
    by a single character.
    '''

    def __init__(self,chars):
        '''
        Arguments:
        chars - The characters representing each direction.  They should be in the
        order SW S SE W E NW N NE.
        '''
        ords = map(ord,chars)
        self.to_trans = dict(zip(ords, SemaphoreInputMode.numpad_ords))
        self.from_trans = dict(zip(SemaphoreInputMode.numpad_ords, ords))

    def to_numpad(self,x):
        return unicode(x).translate(self.to_trans)

    def from_numpad(self,x):
        return unicode(x).translate(self.from_trans)

SEMAPHORE_INPUT_NUMPAD = SemaphoreTranslateInput(SemaphoreInputMode.numpad_chars)
SEMAPHORE_INPUT_PHONEPAD = SemaphoreTranslateInput('78946123')
SEMAPHORE_INPUT_VI = SemaphoreTranslateInput('bjnhlyku')
SEMAPHORE_INPUT_ARROW = SemaphoreTranslateInput(u'↙↓↘←→↖↑↗')

class SemaphoreEncoder(lex_base.Encoder):
    u'''Encodes text to semaphore.

        >>> enc = SemaphoreEncoder()
        >>> print enc('hello')
        ←↙ ↗↓ ↙↗ ↙↗ ↖←
    '''

    states = (
        ('num','exclusive'),
    )

    tokens = (
        'ALNUM',
        'WHITESPACE',
        'CHANGEMODE',
    )

    def __init__(self,**kwargs):
        '''
        Keyword arguments:
        ``sep`` - Character separator.  Default is ' '.
        ``wsep`` - Word separator.  Default is '/'.
        ``input_mode`` - The representation of semaphore directions.   Supported input modes are:
        * ``SEMAPHORE_INPUT_NUMPAD`` - represents directions by numpad keys (down left = 1, down = 2, etc)
        * ``SEMAPHORE_INPUT_PHONEPAD`` - represents directions by telephone pad keys (up left = 1, up = 2, etc)
        * ``SEMAPHORE_INPUT_VI`` - represents directions by vi keys (left = h, down = j, etc)
        * ``SEMAPHORE_INPUT_ARROW`` (default) - represents directions by Unicode arrow characters (left = U+2190, up = U+2191, etc)
        '''
        self.input_mode = kwargs.pop('input_mode',SEMAPHORE_INPUT_ARROW)
        super(SemaphoreEncoder,self).__init__(**kwargs)

    def __call__(self,s):
        '''Converts the string s to semaphore.'''
        return self.input_mode.from_numpad(super(SemaphoreEncoder,self).__call__(s))

    def t_ALNUM(self,t):
        r'[A-Za-z]'
        t.value = to_semaphore[t.value.upper()]
        return t

    def t_num_ALNUM(self,t):
        r'\d'
        if t.value == '0':
            t.value = to_semaphore['K']
        else:
            t.value = to_semaphore[chr(ord(t.value)-ord('1')+ord('A'))]
        return t

    def t_CHANGEMODE(self,t):
        r'(?=\d)'
        t.value=to_semaphore['#']
        t.lexer.begin('num')
        return t

    def t_num_CHANGEMODE(self,t):
        r'(?=\D)'
        t.value=to_semaphore['J']
        t.lexer.begin('INITIAL')
        return t

class SemaphoreDecoder(lex_base.Decoder):
    '''
    Decodes text from semaphore.
    
        >>> dec = SemaphoreDecoder()
        >>> print dec('61 12 13 71 72 / 43 12 32 92 43')
        MANIC SAGES
    '''

    states = (
        ('num', 'exclusive'),
    )

    tokens = (
        'SEMAPHORE',
        'WORDSEP',
        'CHMODE',
    )

    def __init__(self,**kwargs):
        '''
        Keyword arguments:
        ``sep`` - Character separator.  Default is ' '.
        ``wsep`` - Word separator.  Default is '/'.
        ``input_mode`` - The representation of semaphore directions.   Supported input modes are:
        * ``SEMAPHORE_INPUT_NUMPAD`` (default) - represents directions by numpad keys (down left = 1, down = 2, etc)
        * ``SEMAPHORE_INPUT_PHONEPAD`` - represents directions by telephone pad keys (up left = 1, up = 2, etc)
        * ``SEMAPHORE_INPUT_VI`` - represents directions by vi keys (left = h, down = j, etc)
        * ``SEMAPHORE_INPUT_ARROW`` - represents directions by Unicode arrow characters (left = U+2190, up = U+2191, etc)
        '''
        self.input_mode = kwargs.pop('input_mode',SEMAPHORE_INPUT_NUMPAD)
        super(SemaphoreDecoder,self).__init__(**kwargs)

    def __call__(self,s):
        '''Converts the string s from semaphore to plain text.'''
        return super(SemaphoreDecoder,self).__call__(self.input_mode.to_numpad(s))
   
    def t_SEMAPHORE(self,t):
        r'[1-46-9]{2}'
        t.value=from_semaphore[t.value]
        if t.value=='#':
            t.lexer.begin('num')
            return None
        else:
            return t

    def t_num_SEMAPHORE(self,t):
        r'[1-46-9]{2}'
        tmp = from_semaphore[t.value]
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
