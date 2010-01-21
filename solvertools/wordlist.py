from __future__ import with_statement
from util import get_dictfile
import os, sys, re, codecs

def identity(s):
    return s

def ensure_unicode(s):
    if isinstance(s, str):
        return s.decode('utf-8')

def case_insensitive(s):
    return ensure_unicode(s).upper()

def comma_separated(s):
    return s.split(',', 1)

def alphanumerics_only(s):
    return re.sub("[^A-Z0-9]", "", case_insensitive(s))

class Wordlist(object):
    """
    A lazily-loaded wordlist.

    Words are represented as a dictionary, mapping each word in the list to
    a number that is intended to represent the word's frequency. For wordlists
    that do not include frequency information, the frequency will be 1.

    Wordlists are intended to be read-only. You index them as if they were
    dictionaries.
    """
    def __init__(self, filename, convert=case_insensitive, reader=identity):
        """
        Load a wordlist given a filename.

        You should provide a `convert` function, representing how to convert
        an arbitrary string to the format you want. It will be applied to all
        words in the wordlist, in addition to strings you query it with later.
        The default convert function ensures that all strings are Unicode and
        collapses case.

        If you want case to matter, use `ensure_unicode` as the convert
        function. Using `identity` is just asking for trouble the moment you
        encounter a stray umlaut.
        """
        self.filename = filename
        self.words = None
        self.sorted = None
        self.convert = convert
        self.reader = reader

    def variant(self, convert=None, reader=None):
        """
        If you want to get the same dictionary, but with a different conversion
        function or (for some reason) a different line reader, use its .variant
        method.

        For example, if you want a version of the NPL wordlist that omits
        punctuation and spaces, you can ask for
        NPL.variant(alphanumerics_only).
        """
        if convert is None: convert = self.convert
        if reader is None: reader = self.reader
        return Wordlist(self.filename, convert, reader)

    # load the data when necessary
    def _load(self):
        self.words = {}
        with codecs.open(get_dictfile(self.filename), 'utf-8') as wordlist:
            entries = [self.reader(line.strip()) for line in wordlist]
            for entry in entries:
                if isinstance(entry, tuple):
                    # this word has a frequency attached
                    word, val = entry
                    self.words[self.convert(word)] = val
                else:
                    self.words[self.convert(entry)] = 1

            # Sort the words by reverse frequency if possible,
            # then alphabetically
            self.sorted = sorted(self.words.keys(),
              key=lambda word: (-self.words[word], word))
    
    # Implement the read-only dictionary methods
    def __iter__(self):
        "Yield the wordlist entries in sorted order."
        if self.words is None: self._load()
        return iter(self.sorted)

    def __iteritems__(self):
        "Yield the wordlist entries and their frequencies in sorted order."
        if self.words is None: self._load()
        for word in self.sorted:
            yield (word, self.words[word])

    def __contains__(self, word):
        """
        Check if a word is in the list. This applies the same `convert`
        function that was used to build the list to the word.
        """
        if self.words is None: self._load()
        return self.convert(word) in self.words
    
    def __getitem__(self, word):
        """
        Get a word's frequency in the list. This applies the same `convert`
        function that was used to build the list to the word.
        """
        if self.words is None: self._load()
        return self.words[self.convert(word)]
    
    def get(self, word, default=None):
        if self.words is None: self._load()
        return self.words.get(self.convert(word))

    def keys(self):
        if self.words is None: self._load()
        return self.sorted

    def __repr__(self):
        return "Wordlist(%r, %s)" % (self.filename, self.convert.__name__)
    def __str__(self):
        return repr(self)
    def __hash__(self):
        return hash((self.convert, self.filename))
    def __cmp__(self, other):
        if self.__class__ != other.__class__: return -1
        return cmp((self.filename, self.convert),
                   (other.filename, other.convert))

# Define two useful wordlists
ENABLE = Wordlist('enable.txt', case_insensitive)
NPL = Wordlist('npl_allwords2.txt', case_insensitive)

