from bayesinator.core import *
import math
from solvertools.csvfile import read_csv
from solvertools.util import get_datafile



elements = [e for e in read_csv(get_datafile("codes/elements.txt"))]
element_symbols = set([e.symbol.capitalize() for e in elements])
element_names = set([e.name.capitalize() for e in elements])
max_protons = max([int(e.z) for e in elements])
element_entropy = math.log(max_protons, 2)

@puzzle_property(basestring)
def element_symbol(s):
    return s.capitalize() in element_symbols

@puzzle_property(basestring)
def element_name(s):
    return s.capitalize() in element_names

@puzzle_property(int)
def element_index(n):
    return 0 <= n <= max_protons

@entropy_function(element_symbol)
def element_symbol_entropy(e):
    return element_entropy

@entropy_function(element_name)
def element_name_entropy(e):
    return element_entropy

@entropy_function(element_index)
def element_index_entropy(e):
    return element_entropy



amino_acids = [e for e in read_csv(get_datafile("codes/amino.txt"))]
amino_acid_names = set([e.amino_acid.capitalize() for e in amino_acids])
amino_acid_3ltr_abrs = set([e['3_letter'].capitalize() for e in amino_acids])
amino_acid_1ltr_abrs = set([e['1_letter'].capitalize() for e in amino_acids])
amino_acid_entropy = math.log(len(amino_acids), 2)

@puzzle_property(basestring)
def amino_acid_name(s):
    return s.capitalize() in amino_acid_names

@puzzle_property(basestring)
def amino_acid_3ltr_abr(s):
    return s.capitalize() in amino_acid_3ltr_abrs

@puzzle_property(basestring)
def amino_acid_1ltr_abr(s):
    return s.capitalize() in amino_acid_1ltr_abrs

@entropy_function(amino_acid_name)
def amino_acid_name_entropy(acid):
    return amino_acid_entropy

@entropy_function(amino_acid_3ltr_abr)
def amino_acid_3ltr_abr_entropy(acid):
    return amino_acid_entropy

@entropy_function(amino_acid_1ltr_abr)
def amino_acid_1ltr_abr_entropy(acid):
    return amino_acid_entropy
