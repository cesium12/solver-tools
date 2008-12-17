import solver
import itertools
from model.numbers import number_logprob
from model.language_model import english_model
from math import log
from recognize import characters
import string

@solver.register_transform
def trans_take_first_letters(puzzle):
    if not isinstance(puzzle, tuple):
        return
    foo = ""
    for s in puzzle:
        if not isinstance(s, str) or len(s) < 1:
            return
        foo = foo + s[0]
    yield (2,foo,"take first letters")

@solver.register_transform
def trans_take_second_letters(puzzle):
    if not isinstance(puzzle, tuple):
        return
    foo = ""
    for s in puzzle:
        if not isinstance(s, str) or len(s) < 2:
            return
        foo = foo + s[1]
    yield (10,foo,"take second letters")

def trans_take_item_n(puzzle):
    if not isinstance(puzzle, tuple):
        return
    for n in itertools.count():
        collected = []
        for item in puzzle:
            if not isinstance(item, tuple) or len(item) < 1:
                return
            collected.append(item[n])
        yield (-number_logprob(n), tuple(collected), "take item %d" % n)

@solver.register_transform
def trans_sort(puzzle):
    if isinstance(puzzle, tuple):
        yield (2, sorted(puzzle))
    return

@solver.register_transform
def trans_sort_by_length(puzzle):
    if not isinstance(puzzle, tuple):
        return
    yield (4, tuple(b for (a,b) in sorted([(len(s),s) for s in puzzle])),
              "sort by length")

@solver.register_transform
def trans_diagonalize(puzzle):
    if not isinstance(puzzle, tuple):
        return
    foo = ""
    for i in range(len(puzzle)):
        if not isinstance(puzzle[i],str):
            return
        if len(puzzle[i]) <= i:
            return
        foo = foo + puzzle[i][i]
    yield (2, foo, "diagonalize")

@solver.register_transform
def trans_reverse(puzzle):
    if not isinstance(puzzle, tuple):
        return
    yield (3, reversed(puzzle), "reverse")

def caesar_shift(text, n):
    def caesar_char(char, n):
        if char not in string.uppercase: return char
        before = ord(char) - ord('A')
        after = (before+n) % 26
        return chr(ord('A')+after)
    return ''.join(caesar_char(c, n) for c in text)

@solver.register_transform
def trans_optimal_caesar(puzzle):
    if not isinstance(puzzle, str): return
    length = characters(puzzle)
    best_score = -1000
    best_n = 0
    for n in range(26):
        shifted = caesar_shift(puzzle, n)
        score = english_model.text_logprob(shifted)
        if score > best_score:
            best_score = score
            best_n = n
    shift_a = caesar_shift('A', best_n)
    yield (2+(log(26)/log(2)/length), (shift_a, caesar_shift(puzzle, best_n)),
           "Caesar shift A->%s" % shift_a)

def demo():
    print list(trans_optimal_caesar('ECGUCT'))

if __name__ == '__main__': demo()
