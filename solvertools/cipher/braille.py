from solvertools.alphabet import ALPHABETS as _ALPHABETS

from cStringIO import StringIO

BRAILLE = _ALPHABETS['braille']
ENGLISH = _ALPHABETS['english']

def code_to_braille(code):
    return unichr(0x2800+code)

def code_to_english(code):
    return braille_to_english(code_to_braille(code))

def braille_to_english(braille):
    return ENGLISH[BRAILLE.index(braille)]

def english_to_braille(ch):
    return BRAILLE[ENGLISH.index(ch)]

def braille_to_code(braille):
    return ord(braille)-0x2800

def possible_letters(code,mask):
    """
    Returns the possible letters for a Braille block for which we have partial
    knowledge.
    """
    io = StringIO()
    for ch in BRAILLE:
        if (braille_to_code(ch))&mask==code&mask:
            io.write(braille_to_english(ch))
    return io.getvalue()
   
def grid_code(*args):
    factor = 1
    code = 0
    for arg in args:
        if(arg):
            code += factor
        factor *= 2
    return code

def grid_letters(*args):
    return code_to_english(grid_code(*args))

def grid_code_uncertain(*args):
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

def grid_possible(*args):
    return possible_letters(*grid_code_uncertain(*args))

def grid_to_codes(grid):
    """
    Convert Braille to English letters.  Takes a list of lists in column
    major format.  Entries that evaluate to True are assumed to be dots.
    Returns a list of lists of Braille codes offsets ( 0 = U+2800, 1 = U+2801, etc. ).
    """
    return parse_grid(grid,grid_code)

def grid_to_codes_uncertain(grid):
    """
    Like grid_to_codes, but entries that are equal to None are assumed to be
    unknown.  Returns a grid of tuples
    """
    return parse_grid(grid,grid_code_uncertain)

def grid_to_letters(grid):  
    return parse_grid(grid,grid_letters)

def grid_to_possible_letters(grid):
    return parse_grid(grid,grid_possible)

def parse_grid(grid,func):
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
