from __future__ import with_statement
import os
import sys
import re

def module_path():
    "Figure out the full path of this file."
    return os.path.dirname(unicode(__file__, sys.getfilesystemencoding( )))

package_dir = os.path.dirname(module_path())

def get_datafile(path):
    "Get a file from the data directory."
    return os.path.sep.join([module_path(), 'data', 'dict', path])

def identity(s):
    return s

def case_insensitive(s):
    return s.upper()

def comma_separated(s):
    return s.split(',', 1)

def alphanumerics_only(s):
    return re.sub("[^A-Z0-9]", "", s.upper())

class Wordlist(object):
    def __init__(self, filename, conv=case_insensitive, reader=identity):
        self.filename = filename
        self.words = None
        self.sorted = None
        self.convert = conv
        self.reader = reader

    def _load(self):
        self.words = {}
        with open(get_datafile(self.filename)) as wordlist:
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

    def __repr__(self):
        return "Wordlist(%r)" % (self.filename)
    def __str__(self):
        return repr(self)

ENABLE = Wordlist('enable.txt')
