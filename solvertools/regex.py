"""
Wacky tools for slicing and dicing regexes.
"""
from sre_parse import parse, CATEGORIES, SubPattern
from sre_constants import MAXREPEAT

REVERSE_CATEGORIES = {}
for key, value in CATEGORIES.items():
    REVERSE_CATEGORIES[str(value)] = key

def regex_index(regex, index):
    return unparse(_regex_index(parse(regex), index))

def regex_len(regex):
    return _regex_len(parse(regex))

def _regex_index(struct, index):
    lo_counter = hi_counter = 0
    choices = []
    for sub in struct:
        lo, hi = _regex_len(sub)
        lo_counter += lo
        hi_counter += hi
    raise NotImplementedError

def unparse(struct):
    if isinstance(struct, (list, SubPattern)):
        return u''.join(unparse(x) for x in struct)
    elif isinstance(struct, tuple):
        opcode, data = struct
        if str(struct) in REVERSE_CATEGORIES:
            return REVERSE_CATEGORIES[str(struct)]
        elif 'unparse_%s' % opcode in globals():
            unparser = globals()['unparse_%s' % opcode]
            return unparser(data)
        else:
            raise ValueError("I don't know what to do with this regex: "
                             + str(struct))
    else:
        raise TypeError("%s doesn't belong in a regex structure" % struct)

def unparse_literal(data):
    return unichr(data)

def unparse_any(data):
    return u'.'

def unparse_range(data):
    start, end = data
    return unichr(start) + u'-' + unichr(end)

def unparse_in(data):
    return u'[' + unparse(data) + u']'

def unparse_category(data):
    fake_value = ('in', [('category', data)])
    return REVERSE_CATEGORIES[data]

def unparse_subpattern(data):
    return u'(' + unparse(data[1]) + u')'

def unparse_branch(data):
    return u'|'.join(unparse(branch) for branch in data[1])

def unparse_max_repeat(data):
    lo, hi, value = data
    if lo == 0 and hi == MAXREPEAT:
        symbol = u'*'
    elif lo == 0 and hi == 1:
        symbol = u'?'
    elif lo == 1 and hi == MAXREPEAT:
        symbol = u'+'
    else:
        symbol = u'{%d,%d}' % (lo, hi)
    return unparse(value) + symbol

