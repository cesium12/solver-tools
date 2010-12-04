"""
Utilities for ciphers where one character maps to a string of several characters
(e. g. Morse code, semaphore)
"""

import re
from ply import lex

import logging
logger = logging.getLogger(__name__)

def reverse(d):
    return dict((v,k) for k, v in d.iteritems())

def wsep_regex(wsep):
    if wsep is not None:
        return re.escape(wsep)
    else:
        return r'\s+'

class CoderCommon(object):

    def __init__(self):
        self.lexer = lex.lex(module=self,debuglog=logger,errorlog=logger)

    def t_ANY_error(self,t):
        t.lexer.skip(1)

class Encoder(CoderCommon):

    def __init__(self,**kwargs):
        self.sep=kwargs.get('sep',' ')
        self.wsep=kwargs.get('wsep','/')
        super(Encoder,self).__init__()

    def __call__(self,s):
        self.lexer.input(s)
        return self.sep.join(map(lambda t: t.value,self.lexer))

    def t_ANY_WHITESPACE(self,t):
        r'\s+'
        if self.wsep:
            t.value=self.wsep
        return t

class Decoder(CoderCommon):

    def __init__(self,**kwargs):
        # we need to create a new function so we can set its docstring
        self.wsep = kwargs.get('wsep','/')
        self.t_ANY_WORDSEP = lambda t : self._t_ANY_WORDSEP(t)
        self.t_ANY_WORDSEP.__doc__ = wsep_regex(self.wsep)
        self.t_ANY_ignore = kwargs.get('sep',' ')
        super(Decoder,self).__init__()
    
    def __call__(self,s):
        self.lexer.input(s)
        return ''.join(map(lambda t: t.value,self.lexer))

    def _t_ANY_WORDSEP(self,t):
        if self.wsep is not None:
            t.value=' '
        return t

