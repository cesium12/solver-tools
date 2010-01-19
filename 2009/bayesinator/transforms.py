import solver
import itertools
from recognize import puzzle_logprob
from model.numbers import number_logprob
from model.language_model import english_model
from math import log
import string

@solver.register_transform
def trans_take_first_letters(puzzle):
    if not isinstance(puzzle, tuple):
        return
    letters = ""
    leftover_logprob = 0.0
    for s in puzzle:
        if not isinstance(s, str) or len(s) < 1:
            return
        letters += s[0]
        leftover_logprob += puzzle_logprob(s[1:])
    yield (-2+leftover_logprob,letters,"take first letters")

@solver.register_transform
def trans_take_second_letters(puzzle):
    if not isinstance(puzzle, tuple):
        return
    letters = ""
    leftover_logprob = 0.0
    for s in puzzle:
        if not isinstance(s, str) or len(s) < 2:
            return
        letters += s[1]
        leftover_logprob += puzzle_logprob((s[0], s[2:]))
    yield (-10+leftover_logprob,letters,"take second letters")

def trans_take_item_n(puzzle):
    if not isinstance(puzzle, tuple):
        return
    for n in itertools.count():
        collected = []
        leftover_logprob = 0.0
        for item in puzzle:
            if not isinstance(item, tuple) or len(item) < 1:
                return
            collected.append(item[n])
            leftover_logprob += puzzle_logprob((item[:n], item[n+1:]))
        yield (number_logprob(n)+leftover_logprob, tuple(collected), 
               "take item %d" % n)

@solver.register_transform
def trans_sort(puzzle):
    if isinstance(puzzle, tuple):
        yield (-2, sorted(puzzle))
    return

@solver.register_transform
def trans_sort_by_length(puzzle):
    if not isinstance(puzzle, tuple):
        return
    yield (-4, tuple(b for (a,b) in sorted([(len(s),s) for s in puzzle])),
              "sort by length")

@solver.register_transform
def trans_diagonalize(puzzle):
    if not isinstance(puzzle, tuple):
        return
    foo = ""
    leftover_logprob = 0.0
    for i in range(len(puzzle)):
        if not isinstance(puzzle[i],str):
            return
        if len(puzzle[i]) <= i:
            return
        foo += puzzle[i][i]
        leftover_logprob += puzzle_logprob(puzzle[i][:i], puzzle[i][i+1:])
    yield (-2+leftover_logprob, foo, "diagonalize")

@solver.register_transform
def trans_reverse(puzzle):
    if not isinstance(puzzle, tuple):
        return
    yield (-3, reversed(puzzle), "reverse")

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
    best_score = -1000
    best_n = 0
    for n in range(26):
        shifted = caesar_shift(puzzle, n)
        score = english_model.text_logprob(shifted)
        if score > best_score:
            best_score = score
            best_n = n
    shift_a = caesar_shift('A', best_n)
    yield (-2-(log(26)/log(2)), (shift_a, caesar_shift(puzzle, best_n)),
           "Caesar shift A->%s" % shift_a)

def demo():
    print list(trans_optimal_caesar('ECGUCT'))

if __name__ == '__main__': demo()
