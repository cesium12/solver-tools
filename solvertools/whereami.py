"""
A useful module for loading things relative to where this file is.
"""

import os
import sys

def module_path():
    return os.path.dirname(unicode(__file__, sys.getfilesystemencoding( )))

package_dir = os.path.dirname(module_path())

def get_data(path):
    return package_dir + os.path.sep + 'data' + os.path.sep + path
    
