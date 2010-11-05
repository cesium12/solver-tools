from solvertools.regex import *

def test_regex_length():
    assert regex_len('/foo|bar/') == (3, 3)
    assert regex_len('/(foo)?/') == (0, 3)
    assert regex_len('/fo+o|bar/') == (3, MAXREPEAT)
    assert regex_len('/a?b?c?d?(efg|hijk)/') == (3, 8)
    assert regex_len('/.*/') == (0, MAXREPEAT)
    assert regex_len(r'/\S\s?/') == (1, 2)
    assert regex_len('/^foo$/') == (3, 3)
