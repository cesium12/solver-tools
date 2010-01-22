import os
import sys

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

