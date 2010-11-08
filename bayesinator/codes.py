from bayesinator.core import *
import math
from solvertools.csvfile import read_csv
from solvertools.util import get_datafile



elements = [e for e in read_csv(get_datafile("codes/elements.txt"))]
element_symbols = set([e.symbol.capitalize() for e in elements])
element_names = set([e.element.capitalize() for e in elements])
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



countries = [c for c in read_csv(get_datafile("codes/country.txt"))]
country_names = set([c.name.capitalize() for c in countries])
country_codes = set([c.code.upper() for c in countries])
country_entropy = math.log(len(countries), 2)

@puzzle_property(basestring)
def country_name(s):
    return s.capitalize() in country_names

@puzzle_property(basestring)
def country_code(s):
    return s.upper() in country_codes

@entropy_function(country_name)
def country_name_entropy(s):
    return country_entropy

@entropy_function(country_code)
def country_code_entropy(s):
    return country_entropy



tlds = set([tld.domain.strip('.').upper() for tld in read_csv(get_datafile("codes/tld.txt"))])
tld_entropy = math.log(len(tlds), 2)

@puzzle_property(basestring)
def top_level_domain(s):
    return s.upper() in tlds

@entropy_function(top_level_domain)
def tld_entropy(s):
    return tld_entropy



constellations = [c for c in read_csv(get_datafile("codes/constellations.txt"))]
constellation_names = set([c.constellation.capitalize() for c in constellations])
constellation_genitive = set([c.genitive.capitalize() for c in constellations])
constellation_3ltr_abrs = set([c['3_letter'].capitalize() for c in constellations])
constellation_4ltr_abrs = set([c['4_letter'].capitalize() for c in constellations])
constellation_entropy = math.log(len(constellations), 2)

@puzzle_property(basestring)
def constellation_name(s):
    return s.capitalize() in constellation_names

@puzzle_property(basestring)
def constellation_genitive(s):
    return s.capitalize() in constellation_genitive

@puzzle_property(basestring)
def constellation_3ltr_abr(s):
    return s.capitalize() in constellation_3ltr_abrs

@puzzle_property(basestring)
def constellation_4ltr_abr(s):
    return s.capitalize() in constellation_4ltr_abrs

@entropy_function(constellation_name)
def constellation_name_entropy(s):
    return constellation_entropy

@entropy_function(constellation_genitive)
def constellation_genitive_entropy(s):
    return constellation_entropy

@entropy_function(constellation_3ltr_abr)
def constellation_3ltr_abr_entropy(s):
    return constellation_entropy

@entropy_function(constellation_4ltr_abr)
def constellation_3ltr_abr_entropy(s):
    return constellation_entropy



airports = [port for port in read_csv(get_datafile("codes/airports.txt"))]
airports_iata = set([port.iata.upper() for port in airports])
airports_icao = set([port.icao.upper() for port in airports])

airports_us = [port for port in read_csv(get_datafile("codes/airports-us.txt"))]
airports_us_iata = set([port.iata.upper() for port in airports_us])
airports_us_icao = set([port.icao.upper() for port in airports_us])

airports_major = [port for port in read_csv(get_datafile("codes/airports-us-major.txt"))]
airports_major_iata = set([port.iata.upper() for port in airports_major])
airports_major_icao = set([port.icao.upper() for port in airports_major])

@puzzle_property(basestring)
def airport_code_iata(s):
    return s.upper() in airports_iata

@puzzle_property(basestring)
def airport_code_icao(s):
    return s.upper() in airports_icao
