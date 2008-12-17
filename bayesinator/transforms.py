import solver


@solver.register_transform
def trans_take_first(s):
    if len(s) > 1:
        return [(-2, s[0])]
    return []


@solver.register_transform
def trans_sort(puzzle):
    if isinstance(puzzle, list):
        return [(-2, sorted(puzzle))]
    return []
