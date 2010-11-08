"""
This module provides some general transformations on puzzles.
"""

from bayesinator.core import *



@puzzle_property(basestring)
def has_spaces(s):
    return ' ' in s


@transformation(has_spaces)
def split_on_spaces(s):
    yield s.split()
