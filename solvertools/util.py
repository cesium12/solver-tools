from __future__ import with_statement
import os
import sys
import cPickle as pickle
import logging

def build_path(parts):
    return os.path.sep.join(p for p in parts if p)

def module_path():
    "Figure out the full path of this file."
    return os.path.dirname(unicode(__file__, sys.getfilesystemencoding( )))

package_dir = os.path.dirname(module_path())

def get_datafile(path):
    "Get a file from the data directory."
    return build_path([package_dir, 'data', path])

def get_dictfile(path):
    "Get a file from the data/dict directory."
    return build_path([package_dir, 'data', 'dict', path])

# Simple functions for working with pickles.
# For more awesome pickling, see the pickledir below and lib/persist.py.

def get_picklefile(path):
    return build_path([package_dir, 'data', 'pickle', path])

def load_pickle(path):
    with open(get_picklefile(path)) as f:
        return pickle.load(f)

def save_pickle(obj, path):
    # There's no intuitive order for these arguments, so switch them if
    # necessary.
    if isinstance(obj, basestring) and not isinstance(path, basestring):
        obj, path = path, obj
    with open(get_picklefile(path), 'w') as f:
        pickle.dump(obj, f)

def file_exists(path):
    return os.access(path, os.F_OK)

## interface to PickleDict to include later if we need it
## (might be too complex for what we want)
# PD = PickleDict(build_path([package_dir, 'data', 'pickle', 'pickledict']))

