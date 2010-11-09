"""
Wacky tools for slicing and dicing regexes.
"""
from sre_parse import parse, CATEGORIES, SPECIAL_CHARS, SubPattern
from sre_constants import MAXREPEAT

UNKNOWN = u'/.*/'
INVALID = u'#'

REVERSE_CATEGORIES = {}
for key, value in CATEGORIES.items():
    REVERSE_CATEGORIES[str(value)] = key

def regex_sequence(strings):
    pattern = []
    if any(is_regex(s) for s in strings):
        for s in strings:
            pattern.extend(parse(bare_regex(s)))
        return u'/'+unparse(pattern)+u'/'
    else:
        return u''.join(strings)

def is_regex(text):
    """
    In solvertools, regex inputs are represented as strings that begin and end
    with slashes.
    """
    if not isinstance(text, basestring):
        return False
    return text.startswith(u'/') and text.endswith(u'/')

def strip_slashes(text):
    """
    Remove the slashes that may surround a regex.
    """
    return text.strip(u'/')

def bare_regex(text):
    """
    Removes the slash markers from a regex if it has them.
    """
    if is_regex(text):
        return text[1:-1]
    else:
        return text

def regex_len(regex):
    """
    Returns a tuple of the minimum and maximum possible length string that
    a regex will match. Returns MAXREPEAT (65535) if a match can be
    very or infinitely long.
    """
    if not is_regex(regex):
        return len(regex), len(regex)
    return _regex_len_pattern(parse(bare_regex(regex)))

def _regex_len_pattern(pattern):
    "Returns the minimum and maximum length of a parsed regex pattern."
    lo = hi = 0
    for op, data in pattern:
        if op in ('literal', 'in', 'category', 'any'):
            sub_lo = sub_hi = 1
        elif op == 'subpattern':
            sub_lo, sub_hi = _regex_len_pattern(data[1])
        elif op == 'branch':
            sub_lo, sub_hi = _regex_len_branch(data[1])
        elif op == 'max_repeat':
            sub_lo, sub_hi = _regex_len_repeat(data)
        elif op == 'at':
            sub_lo = sub_hi = 0
        else:
            raise ValueError("I don't know what to do with this regex: "
                             + str(struct))
        lo += sub_lo
        hi += sub_hi
    return lo, min(MAXREPEAT, hi)

def _regex_len_branch(branches):
    """
    Returns the minimum and maximum length of a regex branch.

    This does not take into account the fact that some lengths in between may
    be impossible.
    """
    lo = MAXREPEAT
    hi = 0
    for branch in branches:
        sub_lo, sub_hi = _regex_len_pattern(branch)
        lo = min(lo, sub_lo)
        hi = max(hi, sub_hi)
    return lo, hi

def _regex_len_repeat(data):
    """
    Return the minimum and maximum length of a repeating expression.
    """
    min_repeat, max_repeat, pattern = data
    lo, hi = _regex_len_pattern(pattern)
    return min_repeat * lo, min(MAXREPEAT, max_repeat * hi)

def round_trip(regex):
    return unparse(parse(bare_regex(regex)))

def regex_index(regex, index):
    """
    Index into a regex, returning a smaller regex of the things that match
    in that position.

    The index can be given as a string, in which case it will be converted
    to an int. If the index is itself a regex, this will give up and return
    the uninformative answer /.*/.
    """
    if is_regex(index):
        return UNKNOWN
    elif isinstance(index, basestring):
        try:
            index = int(index)
        except ValueError:
            return INVALID
    elif not is_regex(regex):
        return regex[index]
    choices = _regex_index_pattern(parse(bare_regex(regex)), index)
    if len(choices) == 0:
        # not exactly sure how this would happen
        return INVALID
    elif len(choices) == 1:
        regex = unparse(choices[0])
        if choices[0][0][0] == 'literal':
            # We know our choices are length-1 regexes. If we have one choice,
            # and its one character has the op of 'literal', we can just return
            # the bare literal.
            return regex
        else:
            return u'/%s/' % (regex,)
    else:
        regex = round_trip(unparse(('branch', (None, choices))))
        return u'/%s/' % (regex,)

def _regex_index(struct, index):
    if isinstance(struct, (list, SubPattern)):
        return _regex_index_pattern(struct, index)
    else:
        opcode, data = struct
        if opcode in ('literal', 'in', 'category', 'any'):
            if index == 0:
                return [[struct]]
            else:
                return []
        elif opcode == 'subpattern':
            return _regex_index_pattern(data[1], index)
        elif opcode == 'branch':
            return _regex_index_branch(data[1], index)
        elif opcode == 'max_repeat':
            return _regex_index_repeat(data, index)
        else:
            raise ValueError("I don't know what to do with this regex: "
                             + str(struct))

def regex_slice(expr, start, end):
    """
    Get a slice of a string, which may be an uncertain regex, by calling
    regex_index on each index.

    Note that this can return expressions that are overly general: for example,
    it can mix characters from both branches of a regex. Being more specific
    than that would take more work.
    """
    if not is_regex(expr):
        return expr[slice(start, end)]
    if start < 0 or end < 0:
        raise NotImplementedError("Can't take negative slices of a regex yet")
    result = u''
    nonliteral_found = False
    for index in xrange(start, end):
        choices = _regex_index_pattern(parse(bare_regex(expr)), index)
        if choices == INVALID or len(choices) == 0:
            return INVALID
        elif len(choices) == 1:
            regex = unparse(choices[0])
            if choices[0][0][0] != 'literal':
                nonliteral_found = True
            result += regex
        else:
            regex = round_trip(unparse(('branch', (None, choices))))
            if u'|' in regex:
                result +=  u'(%s)' % (regex,)
            else:
                result += regex
    if nonliteral_found:
        return u'/%s/' % result
    else:
        return result

def _regex_index_branch(branches, index):
    choices = []
    for branch in branches:
        choices.extend(_regex_index_pattern(branch, index))
    return choices

def _regex_index_repeat(data, index):
    min_repeat, max_repeat, pattern = data
    lo, hi = _regex_len_pattern(pattern)
    lo = max(lo, 1) # we don't care about things that take up 0 characters
    max_relevant_repeat = min(index // lo + 1, max_repeat)
    newpattern = list(pattern) * max_relevant_repeat
    return _regex_index_pattern(newpattern, index)

def _regex_index_pattern(pattern, index):
    if isinstance(index, slice):
        # we might come up with a clever way to do this
        raise NotImplementedError

    if index < 0:
        # This is an easier case that's still not done yet
        raise NotImplementedError

    lo_counter = hi_counter = 0
    choices = []
    for sub in pattern:
        lo, hi = _regex_len_pattern([sub])
        next_lo = lo_counter + lo
        next_hi = hi_counter + hi
        if index < lo_counter:
            break
        elif lo_counter <= index < next_hi:
            for offset in xrange(lo_counter, hi_counter+1):
                sub_index = index - offset
                if sub_index >= 0:
                    choices.extend(_regex_index(sub, sub_index))
        lo_counter, hi_counter = next_lo, next_hi
    
    # if any of the choices is 'any', it overrules everything else.
    for choice in choices:
        # make sure our choices are single characters
        assert len(choice) == 1
        op, data = choice[0]
        if op == 'any':
            return [choice]
    return choices

def unparse(struct):
    if isinstance(struct, (list, SubPattern)):
        return u''.join(unparse(x) for x in struct)
    elif isinstance(struct, tuple):
        opcode, data = struct
        if str(struct) in REVERSE_CATEGORIES:
            return REVERSE_CATEGORIES[str(struct)]
        elif '_unparse_%s' % opcode in globals():
            unparser = globals()['_unparse_%s' % opcode]
            return unparser(data)
        else:
            raise ValueError("I don't know what to do with this regex: "
                             + str(struct))
    else:
        raise TypeError("%s doesn't belong in a regex structure" % struct)

def _unparse_literal(data):
    char = unichr(data)
    if char in SPECIAL_CHARS:
        return u'\\' + char
    else:
        return char


def _unparse_any(data):
    return u'.'

def _unparse_range(data):
    start, end = data
    return unichr(start) + u'-' + unichr(end)

def _unparse_in(data):
    return u'[' + unparse(data) + u']'

def _unparse_category(data):
    fake_value = ('in', [('category', data)])
    return REVERSE_CATEGORIES[data]

def _unparse_subpattern(data):
    return u'(' + unparse(data[1]) + u')'

def _unparse_branch(data):
    return u'|'.join(unparse(branch) for branch in data[1])

def _unparse_max_repeat(data):
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

def _unparse_at(data):
    if data == 'at_beginning':
        return u'^'
    elif data == 'at_end':
        return u'$'
    else:
        raise ValueError

