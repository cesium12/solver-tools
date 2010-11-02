"""
This class is designed to represent values that show up in puzzles -- not just
strings, but strings with uncertainty, strings with holes in them, and so on.

Note that most of this module is repetitive, boring boilerplate.
"""

import string

def string_op(op, value):
    """
    Perform an operation that expects strings on something that might not
    actually be a string.
    """
    if isinstance(value, FlagValue):
        return value.string_op(op)
    else:
        return op(unicode(value))

def passes_alphanumeric_filter(char):
    """
    Is this character a letter, a number, or a FlagValue?
    """
    if isinstance(char, FlagValue):
        return True
    else:
        char = unicode(char)
        return (char in string.letters or char in string.digits)

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
    return PuzzleString([item for item in seq
                         if passes_alphanumeric_filter(item)])

def regex_value(item):
    """
    Represent how a value would appear in a regex.
    """
    if isinstance(item, basestring):
        return item
    elif isinstance(item, FlagValue):
        return item.as_regex()
    else:
        return unicode(item)

class FlagValue(object):
    """
    The parent class of entries that aren't supposed to be literal
    values, but are supposed to flag that something else is going on.
    """
    def as_regex(self):
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

    def string_op(self, op):
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
    
    def as_regex(self):
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

    def as_regex(self):
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

    def as_regex(self):
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

    def string_op(self, op):
        return ChoiceValue([string_op(op, item) for item in self.choices])

class InvalidValue(FlagValue):
    """
    An object that represents an invalid result, such as indexing past the
    end of an answer.
    """
    def __str__(self):
        return '###'
    
    def __unicode__(self):
        return u'###'

    def as_regex(self):
        # too bad we can't make a character that never matches
        return u'#'
    
    def __repr__(self):
        return 'INVALID'

    def __getitem__(self, index):
        return INVALID

INVALID = InvalidValue()

class PuzzleString(object):
    """
    Acts like a Unicode string, but can contain FlagValues instead of just
    characters.
    
    The constructor will return you a plain Unicode string if it is made of
    plain old characters, even decoding utf-8 if necessary.
    """
    def __new__(cls, chars):
        if all(isinstance(char, str) for char in chars):
            return ''.join(chars).decode('utf-8', 'ignore')
        elif all(isinstance(char, basestring) for char in chars):
            return u''.join(chars)
        else:
            return object.__new__(cls)
    
    def __init__(self, chars):
        self.chars = tuple(chars)
    
    def __str__(self):
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        return u''.join(regex_value(char) for char in self.chars)
    
    def __repr__(self):
        return "PuzzleString(%r)" % (self.chars,)
    
    def __hash__(self):
        return hash(unicode(self))

    def __cmp__(self, other):
        return cmp((str(type(self)), unicode(self))
                   (str(type(other)), unicode(other)))

    def __iter__(self):
        return iter(self.chars)

    def __getitem__(self, index):
        return self.chars[index]

    def string_op(self, op):
        return PuzzleString([op(item) for item in self.chars])

    def upper(self):
        return self.string_op(str.upper)

    def lower(self):
        return self.string_op(str.lower)
