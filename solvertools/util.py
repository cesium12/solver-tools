import os
import sys

def module_path():
    "Figure out the full path of this file."
    return os.path.dirname(unicode(__file__, sys.getfilesystemencoding( )))

package_dir = os.path.dirname(module_path())

def get_datafile(path):
    "Get a file from the data directory."
    return os.path.sep.join([module_path(), 'data', path])

def get_dictfile(path):
    "Get a file from the data/dict directory."
    return os.path.sep.join([module_path(), 'data', 'dict', path])

