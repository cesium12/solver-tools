"""
This module provides some general transformations on puzzles.
"""

from bayesinator.core import *
from bayesinator.language import superstring_entropy



@puzzle_property(basestring)
def has_spaces(s):
    return ' ' in s


@transformation(has_spaces)
def split_on_spaces(s):
    yield s.split()
