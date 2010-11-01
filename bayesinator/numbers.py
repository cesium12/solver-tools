from bayesinator.core import *
import math

@puzzle_property(int)
def even(x):
    return (x % 2) == 0

@entropy_function(int)
def integer_bits(x):
    return 1+math.log(abs(x)+1,2)
