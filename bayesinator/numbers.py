from bayesinator.core import *
from solvertools.model.numbers import number_logprob

@puzzle_property(int)
def is_1_to_26(x):
    return 1 <= x <= 26

@entropy_function(int)
def integer_entropy(n):
    return -number_logprob(n)
