"""
This module contains useful utilities, especially for working with external
files.
"""

from __future__ import with_statement
import os
import sys
import cPickle as pickle
import unicodedata

def asciify(text):
    """
    A wonderfully simple function to remove accents from characters, and
    discard other non-ASCII characters. Outputs a plain ASCII string.
    """
    if not isinstance(text, unicode):
        text = text.decode('utf-8', 'ignore')
    return unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore')

def _build_path(parts):
    "Make a path out of the given path fragments."
    return unicode(os.path.sep.join(p for p in parts if p)).encode('utf-8')

def module_path():
    """Figures out the full path of the directory containing this file.
    
    `PACKAGE_DIR` becomes the parent of that directory, which is the root
    of the solvertools package."""
    return os.path.dirname(unicode(__file__, sys.getfilesystemencoding( )))

PACKAGE_DIR = os.path.dirname(module_path())

def get_datafile(path):
    "Get a complete path for a file in the data directory."
    return _build_path([PACKAGE_DIR, 'data', path])

def get_dictfile(path):
    "Get a complete path for a file in the data/dict directory."
    return _build_path([PACKAGE_DIR, 'data', 'dict', path])

def get_db(path):
    "Get a path for a SQLite database in the data/db directory."
    return _build_path([PACKAGE_DIR, 'data', 'db', path])

# Simple functions for working with pickles.
# For more awesome pickling, see the pickledir below and lib/persist.py.

def get_picklefile(path):
    "Get a complete path for a file in the data/pickle directory."
    return _build_path([PACKAGE_DIR, 'data', 'pickle', path])

def load_pickle(path):
    "Load a pickled object, given its file path (instead of an open file)."
    with open(get_picklefile(path)) as infile:
        return pickle.load(infile)

def save_pickle(obj, path):
    "Save a pickled object, given the object and the file path to save to."
    # There's no intuitive order for these arguments, so switch them if
    # necessary.
    if isinstance(obj, basestring) and not isinstance(path, basestring):
        obj, path = path, obj
    with open(get_picklefile(path), 'w') as outfile:
        pickle.dump(obj, outfile)

def file_exists(path):
    "Test whether a given file exists. You must specify the full path."
    return os.access(path, os.F_OK)

## interface to PickleDict to include later if we need it
## (might be too complex for what we want)
# PD = PickleDict(_build_path([PACKAGE_DIR, 'data', 'pickle', 'pickledict']))

