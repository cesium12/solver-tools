from __future__ import with_statement
import os
import sys
import cPickle as pickle

def _build_path(parts):
    return os.path.sep.join(p for p in parts if p)

def module_path():
    """Figures out the full path of the directory containing this file.
    
    `package_dir` becomes the parent of that directory, which is the root
    of the solvertools package."""
    return os.path.dirname(unicode(__file__, sys.getfilesystemencoding( )))

package_dir = os.path.dirname(module_path())

def get_datafile(path):
    "Get a complete path for a file in the data directory."
    return _build_path([package_dir, 'data', path])

def get_dictfile(path):
    "Get a complete path for a file in the data/dict directory."
    return _build_path([package_dir, 'data', 'dict', path])

# Simple functions for working with pickles.
# For more awesome pickling, see the pickledir below and lib/persist.py.

def get_picklefile(path):
    "Get a complete path for a file in the data/pickle directory."
    return _build_path([package_dir, 'data', 'pickle', path])

def load_pickle(path):
    "Load a pickled object, given its file path (instead of an open file)."
    with open(get_picklefile(path)) as f:
        return pickle.load(f)

def save_pickle(obj, path):
    "Save a pickled object, given the object and the file path to save to."
    # There's no intuitive order for these arguments, so switch them if
    # necessary.
    if isinstance(obj, basestring) and not isinstance(path, basestring):
        obj, path = path, obj
    with open(get_picklefile(path), 'w') as f:
        pickle.dump(obj, f)

def file_exists(path):
    "Test whether a given file exists. You must specify the full path."
    return os.access(path, os.F_OK)

## interface to PickleDict to include later if we need it
## (might be too complex for what we want)
# PD = PickleDict(_build_path([package_dir, 'data', 'pickle', 'pickledict']))

