import solver


@solver.register_transform
def trans_take_first_letters(puzzle):
    if not isinstance(puzzle, list):
        return []
    foo = ""
    for s in puzzle:
        if not isinstance(s, str) or len(s) < 1:
            return []
        foo = foo + s[0]
    return [(2,foo)]

@solver.register_transform
def trans_take_second_letters(puzzle):
    if not isinstance(puzzle, list):
        return []
    foo = ""
    for s in puzzle:
        if not isinstance(s, str) or len(s) < 2:
            return []
        foo = foo + s[1]
    return [(10,foo)]


@solver.register_transform
def trans_sort(puzzle):
    if isinstance(puzzle, list):
        return [(2, sorted(puzzle))]
    return []

@solver.register_transform
def trans_sort_by_length(puzzle):
    if not isinstance(puzzle, list):
        return []
    return [(4, [b for (a,b) in sorted([(len(s),s) for s in puzzle])])]


@solver.register_transform
def trans_diagonalize(puzzle):
    if not isinstance(puzzle, list):
        return []
    foo = ""
    for i in range(len(puzzle)):
        if not isinstance(puzzle[i],str):
            return []
        if len(puzzle[i]) <= i:
            return []
        foo = foo + puzzle[i][i]
    return [(2, foo)]

@solver.register_transform
def trans_reverse(puzzle):
    if not isinstance(puzzle, list):
        return []
    return [(3, reversed(puzzle))]


