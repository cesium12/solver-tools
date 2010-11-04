"""
This class is designed to represent values that show up in puzzles -- not just
strings, but strings with uncertainty, strings with holes in them, and so on.

Note that most of this module is repetitive, boring boilerplate.
"""

import string
REGEX_CHARS = r".\[]{}()*+?^$-"

def string_map(op, value):
    """
    Perform an operation that expects strings on something that might not
    actually be a string.
    """
    if hasattr(value, 'string_map'):
        return value.string_map(op)
    else:
        return op(unicode(value))

def passes_alphanumeric_filter(char):
    """
    Is this character a letter, a number, a FlagValue, or a regex character?
    """
    if isinstance(char, FlagValue):
        return True
    else:
        char = unicode(char)
        return (char in string.letters or char in string.digits or
                char in REGEX_CHARS)

def alphanumeric_filter(seq):
    """
    From a sequence that is most likely a string, extract just the alphanumeric
    characters and the non-characters (which may be placeholders for what will
    eventually be alphanumeric characters).

    This is different from wordlist.alphanumeric_only, which assumes that its
    input is a real Unicode string with nothing weird inside it.
    """
    if isinstance(seq, FlagValue):
        return seq
    return u''.join([unicode(item) for item in seq
                     if passes_alphanumeric_filter(item)])

#def unparse(sre_object):
#    if isinstance(sre_object, list):
#        return ''.join(unparse(x) for x in sre_object)
#    elif isinstance(sre_object, tuple):
#        raise NotImplementedError
#    else:
#        raise TypeError("%s doesn't belong in a compiled regex" % sre_object)

def re_filter(predicate, str_or_regex):
    parsed = sre_parse.parse(str_or_regex)

def to_regex(item):
    """
    Represent how a value would appear in a regex.
    """
    if isinstance(item, basestring):
        return item
    elif isinstance(item, FlagValue):
        return item.to_regex()
    else:
        return unicode(item)

class FlagValue(object):
    """
    The parent class of entries that aren't supposed to be literal
    values, but are supposed to flag that something else is going on.
    """
    def to_regex(self):
        """
        Represent this as a single character if at all possible.
        """
        raise NotImplementedError
    
    def __str__(self):
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        raise NotImplementedError

    def __hash__(self):
        return hash(unicode(self))

    def __cmp__(self, other):
        return cmp((str(type(self)), unicode(self)),
                   (str(type(other)), unicode(other)))
    
    def __getitem__(self, index):
        return INVALID

    def string_map(self, op):
        return self

class NondeterministicValue(FlagValue):
    """
    The parent class of entries that could take many different values.
    """
    pass

class Header(FlagValue):
    """
    An object to designate that a table entry is a header, and not puzzle data
    to be operated on.
    """
    def __init__(self, text):
        if isinstance(text, Header):
            text = text.text
        self.text = text

    def __repr__(self):
        return 'Header(%r)' % (self.text,)

    def __str__(self):
        return unicode(self).encode('utf-8')
    
    def to_regex(self):
        return ''

    def __unicode__(self):
        return u'__%s__' % (self.text,)
    
    def __getitem__(self, other):
        if isinstance(other, Header):
            other = other.text
        return Header(u'%s[%s]' % (self.text, other))

class UnknownValue(NondeterministicValue):
    """
    An object that represents an unknown entry in a table or unknown character
    in a string.
    """
    def __str__(self):
        return '???'

    def __unicode__(self):
        return u'???'

    def to_regex(self):
        return '.'

    def __repr__(self):
        return 'UNKNOWN'

    def __getitem__(self, index):
        return UNKNOWN
UNKNOWN = UnknownValue()

class ChoiceValue(NondeterministicValue):
    """
    This entry could be one of many values.
    """
    def __new__(cls, choices):
        if len(choices) == 0:
            return INVALID
        elif len(choices) == 1:
            return choices[0]
        else:
            return object.__new__(cls)

    def __init__(self, choices):
        self.choices = tuple(choices)

    def to_regex(self):
        return unicode(self)
    
    def __str__(self):
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        return u'(' + (u'|'.join(unicode(choice) for choice in self.choices)) + u')'
    def __repr__(self):
        return 'ChoiceValue(%r)' % (self.choices,)

    def __getitem__(self, index):
        """
        Gets the appropriate item from *each* choice.
        """
        choices = []
        for choice in self.choices:
            try:
                choices.append(choice[index])
            except (TypeError, ValueError, IndexError):
                pass
        return ChoiceValue(choices)

    def string_map(self, op):
        return ChoiceValue([string_map(op, item) for item in self.choices])

class InvalidValue(FlagValue):
    """
    An object that represents an invalid result, such as indexing past the
    end of an answer.
    """
    def __str__(self):
        return '###'
    
    def __unicode__(self):
        return u'###'

    def to_regex(self):
        # too bad we can't make a character that never matches
        return u'#'
    
    def __repr__(self):
        return 'INVALID'

    def __getitem__(self, index):
        return INVALID

INVALID = InvalidValue()
