from solvertools.alphabet import ALPHABETS as _ALPHABETS
from cStringIO import StringIO

'''
Utilities for working with Braille.

This module can represent Braille in two different ways:
either as Unicode characters, or in binary form.

The eight dots of extended Braille are numbered as follows:
``14``
``25``
``36``
``78``
Traditional Braille uses only the first six dots.
The letter D, for example, is represented by the
Braille pattern
``**``
``.*``
``..``
where stars represent raised dots.  Since dots
1,4,5 are raised, the binary representation is
011001, or 25 in base 10.

See also ``solvertools.alphabet.ALPHABETS['braille']``.

    >>> braille_binary_to_english(int('011001',2))
    'D'
    >>> braille_unicode_to_binary(u'\u2825')
    25
    >>> braille_english_to_binary('D')
    25
    >>> braille_grid_to_letters([[1,0,0,1],[0,0,1,0],[0,0,1,0]])
    [[u'A', u'S']]
    >> braille_grid_to_possible_letters([[1,0,None,1],[0,0,1,0],[0,0,1,0]])
    [['A', 'PS']]
'''

_BRAILLE = _ALPHABETS['braille']
_ENGLISH = _ALPHABETS['english']

def braille_binary_to_unicode(code):
    '''Given a binary representation of Braille dots, converts it to unicode.'''
    return unichr(0x2800+code)

def braille_binary_to_english(code):
    '''Given a binary representation of Braille dots, converts it to an English letter.''' 
    return braille_unicode_to_english(braille_binary_to_unicode(code))

def braille_unicode_to_english(braille):
    '''Given a Braille unicode character, returns the corresponding English letter.'''
    return _ENGLISH[_BRAILLE.index(braille)]

def braille_english_to_unicode(ch):
    '''Given an English letter, converts it to a Braille unicode character.'''
    return _BRAILLE[_ENGLISH.index(ch)]

def braille_unicode_to_binary(braille):
    '''Given a Braille unicode character, converts it to binary representation.'''
    return ord(braille)-0x2800

def braille_english_to_binary(ch):
    '''Given an English letter, converts it to a binary Braille representation.'''
    return braille_unicode_to_binary(braille_english_to_unicode(ch))

def braille_possible_letters(code,mask):
    """
    Returns the possible letters for a Braille block for which we have partial
    knowledge.

    Parameters:
    code - the binary representation of the dots that are known to be raised
    mask - the binary representation of the dots that are known
    """
    io = StringIO()
    for ch in _BRAILLE:
        if (braille_unicode_to_binary(ch))&mask==code&mask:
            io.write(braille_unicode_to_english(ch))
    return io.getvalue()
   
def _grid_code(*args):
    factor = 1
    code = 0
    for arg in args:
        if(arg):
            code += factor
        factor *= 2
    return code

def _grid_letters(*args):
    return braille_binary_to_english(_grid_code(*args))

def _grid_code_uncertain(*args):
    factor = 1
    code = 0
    mask = 0
    for arg in args:
        if(arg):
            code += factor
        if(arg is not None):
            mask += factor
        factor *= 2
    return (code, mask)

def _grid_possible(*args):
    return braille_possible_letters(*_grid_code_uncertain(*args))

def braille_grid_to_binary(grid):
    """
    Parses a grid into 3x2 blocks.
    The grid should be input as a list of lists in column
    major format.  Entries that evaluate to True are assumed to be raised dots.
    Returns a list of lists of Braille characters in binary format.
    """
    return _parse_grid(grid,_grid_code)

def braille_grid_to_binary_uncertain(grid):
    """
    Like ``braille_grid_to_binary``, but entries that are equal to None are assumed to be
    unknown.  Returns a list of lists of (binary, mask) pairs.
    """
    return _parse_grid(grid,_grid_code_uncertain)

def braille_grid_to_letters(grid): 
    '''
    Like ``braille_grid_to_binary``, but returns English letters.
    '''
    return _parse_grid(grid,_grid_letters)

def braille_grid_to_possible_letters(grid):
    '''
    Like ``braille_grid_to_binary_uncertain``, but returns English letters.
    '''
    return _parse_grid(grid,_grid_possible)

def _parse_grid(grid,func):
    if(len(grid)==0):
        return []
    width = len(grid[0])
    ans = []
    for y in xrange(0,len(grid),3):
        ansrow = []
        for x in xrange(0,width,2):
            ansrow.append(func(grid[y][x],grid[y+1][x],grid[y+2][x],grid[y][x+1],grid[y+1][x+1],grid[y+2][x+1]))
        ans.append(ansrow)
    return ans
