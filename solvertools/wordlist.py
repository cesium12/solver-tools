"""
The `solvertools.wordlist` module contains a class for working with
lazily-loaded wordlists, along with various string wrangling functions that
ensure you don't have to worry about things like capitalization and encoding.
"""

from __future__ import with_statement
from solvertools.util import get_dictfile, get_picklefile, save_pickle, \
                             load_pickle, file_exists, asciify
from solvertools.regex import is_regex, bare_regex
import re, codecs, unicodedata, logging
logger = logging.getLogger(__name__)

def identity(text):
    "Returns what you give it."
    return text

def _reverse_freq(val):
    "If this value is a number, negate it. Otherwise, leave it alone."
    if isinstance(val, (int, float)):
        return -val
    else:
        return val

def split_accents(text):
    """
    Separate accents from their base characters in Unicode text.
    """
    return unicodedata.normalize('NFKD', text)

def ensure_unicode(text):
    "Given a string of some kind, return the appropriate Unicode string."
    if isinstance(text, str):
        return text.decode('utf-8')
    else: return text

def case_insensitive(text):
    "Collapse case by converting everything to uppercase."
    return ensure_unicode(text).upper()

def case_insensitive_ascii(text):
    "Convert everything to uppercase and discard non-ASCII stuff."
    return asciify(ensure_unicode(text).upper())

def with_frequency(text):
    """
    Use this as a reader when the wordlist has comma-separated entries of the
    form `WORD,freq`.
    """
    word, freq = text.split(',', 1)
    return (word, int(freq))

def with_values(text):
    """
    Use this when each word is associated with one or more values -- for
    example, a phonetic dictionary or a translation dictionary.
    """
    word, valstr = text.split(',', 1)
    values = valstr.split('|')
    return (word, values)

def alphanumeric_only(text):
    """
    Convert everything to uppercase and discard everything but letters and
    digits.
    """
    return re.sub("[^A-Z0-9]", "", case_insensitive_ascii(text))

def letters_only(text):
    """
    Convert everything to uppercase ASCII, and discard everything but the
    letters A-Z.
    """
    return re.sub("[^A-Z]", "", case_insensitive_ascii(text))

def letters_only_unicode(text):
    """
    Convert everything to uppercase, and discard everything that doesn't act
    like a letter (that is, which doesn't have a separate lowercase version).
    Preserve accents and stuff.
    """
    return ''.join(ch for ch in case_insensitive(text)
                   if ch != ch.lower())

def alphabet_filter(alphabet):
    def alphabet_filter_inner(text):
        return ''.join(c for c in case_insensitive(text) if c in alphabet)
    return alphabet_filter_inner

def classical_latin_letters(text):
    "Enforce I=J and U=V as some Latin-themed puzzles do."
    return letters_only(text).replace('U', 'V').replace('J', 'I')

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
    version = 1
    def __init__(self, filename, convert=case_insensitive, reader=identity,
                 pickle=True):
        self.filename = filename
        self.words = None
        self.sorted_words = None
        self.convert = convert
        self.reader = reader
        self.pickle = pickle
        self.regulus = None

    def variant(self, convert=None, reader=None):
        """
        If you want to get the same dictionary, but with a different conversion
        function or (for some reason) a different line reader, use its .variant
        method.

        For example, if you want a version of the NPL wordlist that omits
        punctuation and spaces, you can ask for
        NPL.variant(alphanumerics_only).

        """
        if convert is None:
            convert = self.convert
        if reader is None:
            reader = self.reader
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

    def load_regulus(self):
        """
        If we need to do fast regex operations on this wordlist, we need a
        regulus object. This function ensures that such an object exists.
        """
        if self.words is None:
            self.load()
        logger.info("Loading %s" % self.regulus_name())
        from solvertools.extensions.regulus import regulus
        self.regulus = regulus.Dict()
        loaded_cache = self.regulus.read(self.regulus_name())
        if not loaded_cache:
            del self.regulus
            logger.info("Building %s" % self.regulus_name())
            entries = [regulus.DictEntry(letters_only(word), freq)
                       for word, freq in self.words.iteritems()]
            self.regulus = regulus.Dict(entries)
            logger.info("Saving %s" % self.regulus_name())
            self.regulus.write(self.regulus_name())
    
    def grep(self, pattern):
        """
        Search the wordlist for results matching this pattern.
        Requires the Regulus extension.
        """
        if self.regulus is None:
            self.load_regulus()
        results = self.regulus.grep(str(bare_regex(pattern)))
        return [(result.word, result.freq) for result in results]

    def best_match(self, pattern):
        """
        Search the wordlist for the best result matching this pattern.
        Requires the Regulus extension.
        """
        if not hasattr(self, 'regulus') or self.regulus is None:
            self.load_regulus()
        result = self.regulus.best_match(str(bare_regex(pattern)))
        if result.word is None:
            return (None, 0)
        return result.word, result.freq

    def _load_pickle(self):
        "Load this wordlist from a pickle."
        picklename = self.pickle_name()
        logger.info("Loading %s" % picklename)
        self.words, self.sorted_words = load_pickle(picklename)

    def _load_txt(self):
        "Load this wordlist from a plain text file."
        self.words = {}
        filename = get_dictfile(self.filename+'.txt')
        logger.info("Loading %s" % filename)
        with codecs.open(filename, encoding='utf-8') as wordlist:
            entries = [self.reader(line.strip()) for line in wordlist
                       if line.strip()]
            for entry in entries:
                if isinstance(entry, tuple) or isinstance(entry, list):
                    # this word has a value attached
                    word, val = entry
                    self.words[self.convert(word)] = val
                else:
                    self.words[self.convert(entry)] = 1

            # Sort the words by reverse frequency if possible,
            # then alphabetically

            self.sorted_words = sorted(self.words.keys(),
              key=lambda word: (_reverse_freq(self.words[word]), word))
        picklename = self.pickle_name()
        if self.pickle:
            logger.info("Saving %s" % picklename)
            save_pickle((self.words, self.sorted_words), picklename)
    
    def sorted(self):
        """
        Returns the words in the list in sorted order. The order is descending
        order by frequency, and lexicographic order after that.
        """
        return self.sorted_words

    # Implement the read-only dictionary methods
    def __iter__(self):
        "Yield the wordlist entries in sorted order."
        if self.words is None:
            self.load()
        return iter(self.sorted_words)

    def iteritems(self):
        "Yield the wordlist entries and their frequencies in sorted order."
        if self.words is None:
            self.load()
        for word in self.sorted_words:
            yield (word, self.words[word])

    def __contains__(self, word):
        """
        Check if a word is in the list. This applies the same `convert`
        function that was used to build the list to the word.
        """
        if self.words is None:
            self.load()
        return self.convert(word) in self.words
    
    def __getitem__(self, word):
        """
        Get a word's frequency in the list. This applies the same `convert`
        function that was used to build the list to the word.
        """
        if self.words is None:
            self.load()
        return self.words[self.convert(word)]
    
    def get(self, word, default=None):
        """
        Get the data (frequency) for a word.
        """
        if self.words is None:
            self.load()
        return self.words.get(self.convert(word), default)

    def keys(self):
        """
        Get all the words in the list, in sorted order.
        """
        if self.words is None:
            self.load()
        return self.sorted_words

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

    def regulus_name(self):
        """
        The filename that this wordlist will have when pickled. This is
        determined from its base filename, the name of its convert function,
        and a version number.
        """
        return "%s.%s.%s.regulus" % (self.filename, self.convert.__name__,
                                     self.version)

    def __hash__(self):
        return hash((self.convert, self.filename))

    def __cmp__(self, other):
        if self.__class__ != other.__class__:
            return -1
        return cmp((self.filename, self.convert),
                   (other.filename, other.convert))

# Define useful wordlists
ENABLE = Wordlist('enable', case_insensitive)
NPL = Wordlist('npl_allwords2', case_insensitive)
Google1M = Wordlist('google1M', letters_only, with_frequency)
Google200K = Wordlist('google200K', letters_only, with_frequency)
PHONETIC = Wordlist('phonetic', letters_only, with_values)
COMBINED = Wordlist('sages_combined', letters_only, with_frequency)
LATIN = Wordlist('wikipedia_la', classical_latin_letters, with_frequency)
CHAOTIC = Wordlist('chaotic', letters_only, with_frequency)
#TODO: spanish
