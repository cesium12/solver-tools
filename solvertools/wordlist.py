"""
The `solvertools.wordlist` module contains a class for working with
lazily-loaded wordlists, along with various string wrangling functions that
ensure you don't have to worry about things like capitalization and encoding.
"""

from __future__ import with_statement
from util import get_dictfile, get_picklefile, save_pickle, load_pickle, file_exists
import os, sys, re, codecs, unicodedata, logging
logger = logging.getLogger(__name__)

def identity(s):
    "Returns what you give it."
    return s

def asciify(s):
    """
    A wonderfully simple function to remove accents from characters, and
    discard other non-ASCII characters. Outputs a plain ASCII string.
    """
    return unicodedata.normalize('NFKD', s).encode('ASCII', 'ignore')

def split_accents(s):
    return unicodedata.normalize('NFKD', s)

def ensure_unicode(s):
    "Given a string of some kind, return the appropriate Unicode string."
    if isinstance(s, str):
        return s.decode('utf-8')
    else: return s

def case_insensitive(s):
    "Collapse case by converting everything to uppercase."
    return ensure_unicode(s).upper()

def case_insensitive_ascii(s):
    "Convert everything to uppercase and discard non-ASCII stuff."
    return asciify(ensure_unicode(s).upper())

def with_frequency(s):
    """
    Use this as a reader when the wordlist has comma-separated entries of the
    form `WORD,freq`.
    """
    word, freq = s.split(',', 1)
    return (word, int(freq))

def alphanumeric_only(s):
    """
    Convert everything to uppercase and discard everything but letters and
    digits.
    """
    return re.sub("[^A-Z0-9]", "", case_insensitive_ascii(s))

def letters_only(s):
    "Convert everything to uppercase and discard everything but letters."
    return re.sub("[^A-Z]", "", case_insensitive_ascii(s))

class Wordlist(object):
    """
    A lazily-loaded wordlist.

    Words are represented as a read-only dictionary, mapping each word in the
    list to a number that is intended to represent the word's frequency. For
    wordlists that do not include frequency information, the frequency will be
    1.

    You can use the syntax `word in wordlist` to test whether the wordlist
    contains a given word; `wordlist[word]` will be its frequency. Standard
    methods including `keys()`, `get()`, and `iteritems()` work as well.

    To load a wordlist, call this constructor with the name of
    the wordlist to load, as in `Wordlist("enable")`. Don't give an extension
    or a path, because those depend on whether it's loading from a `.txt` or
    `.pickle` file anyway.
    
    You should also provide a `convert` function,
    representing how to convert an arbitrary string to the format the wordlist
    uses. It will be applied to all words in the wordlist, in addition to
    strings you query it with later.  The default convert function ensures that
    all strings are Unicode and collapses case.

    If you want case to matter, use `ensure_unicode` or `asciify`
    as the convert function. Using `identity` is just asking for trouble
    the moment you encounter a stray umlaut.

    Use the `reader` function to specify how to read a word from each line.
    In most cases, this will be `identity` or `with_frequency`.

    Finally, you can set `pickle=False` if you don't want the wordlist to be
    loaded from or saved to a pickle file.
    """
    def __init__(self, filename, convert=case_insensitive, reader=identity,
                 pickle=True):
        self.filename = filename
        self.words = None
        self.sorted = None
        self.convert = convert
        self.reader = reader
        self.pickle = pickle

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
        return Wordlist(self.filename, convert, reader, pickle=self.pickle)

    # load the data when necessary
    def load(self):
        "Force this wordlist to be loaded."
        if self.pickle and file_exists(get_picklefile(self.pickle_name())):
            return self._load_pickle()
        elif file_exists(get_dictfile(self.filename+'.txt')):
            return self._load_txt()
        else:
            raise IOError("Cannot find a dictionary named '%s'." %
            self.filename)

    def _load_pickle(self):
        picklename = self.pickle_name()
        logger.info("Loading %s" % picklename)
        self.words, self.sorted = load_pickle(picklename)

    def _load_txt(self):
        self.words = {}
        filename = get_dictfile(self.filename+'.txt')
        logger.info("Loading %s" % filename)
        with codecs.open(filename, encoding='utf-8') as wordlist:
            entries = [self.reader(line.strip()) for line in wordlist if line.strip()]
            for entry in entries:
                if isinstance(entry, tuple) or isinstance(entry, list):
                    # this word has a frequency attached
                    word, val = entry
                    self.words[self.convert(word)] = val
                else:
                    self.words[self.convert(entry)] = 1

            # Sort the words by reverse frequency if possible,
            # then alphabetically
            self.sorted = sorted(self.words.keys(),
              key=lambda word: (-self.words[word], word))
        picklename = self.pickle_name()
        if self.pickle:
            logger.info("Saving %s" % picklename)
            save_pickle((self.words, self.sorted), picklename)
    
    def sorted(self):
        """
        Returns the words in the list in sorted order. The order is descending
        order by frequency, and lexicographic order after that.
        """
        return self.sorted

    # Implement the read-only dictionary methods
    def __iter__(self):
        "Yield the wordlist entries in sorted order."
        if self.words is None: self.load()
        return iter(self.sorted)

    def iteritems(self):
        "Yield the wordlist entries and their frequencies in sorted order."
        if self.words is None: self.load()
        for word in self.sorted:
            yield (word, self.words[word])

    def __contains__(self, word):
        """
        Check if a word is in the list. This applies the same `convert`
        function that was used to build the list to the word.
        """
        if self.words is None: self.load()
        return self.convert(word) in self.words
    
    def __getitem__(self, word):
        """
        Get a word's frequency in the list. This applies the same `convert`
        function that was used to build the list to the word.
        """
        if self.words is None: self.load()
        return self.words[self.convert(word)]
    
    def get(self, word, default=None):
        if self.words is None: self.load()
        return self.words.get(self.convert(word), default)

    def keys(self):
        if self.words is None: self.load()
        return self.sorted

    def __repr__(self):
        return "Wordlist(%r, %s, %s)" % (self.filename, self.convert.__name__,
                                         self.reader.__name__)
    def __str__(self):
        return repr(self)
    def pickle_name(self):
        """
        The filename that this wordlist will have when pickled. This is
        determined from its base filename and the names of the functions that
        transformed it.
        """
        return "%s.%s.%s.pickle" % (self.filename, self.convert.__name__,
        self.reader.__name__)
    def __hash__(self):
        return hash((self.convert, self.filename))
    def __cmp__(self, other):
        if self.__class__ != other.__class__: return -1
        return cmp((self.filename, self.convert),
                   (other.filename, other.convert))

# Define two useful wordlists
ENABLE = Wordlist('enable', case_insensitive)
NPL = Wordlist('npl_allwords2', case_insensitive)
Google1M = Wordlist('google1M', letters_only, with_frequency)
Google200K = Wordlist('google200K', letters_only, with_frequency)
COMBINED = Wordlist('sages_combined', alphanumeric_only, with_frequency)
