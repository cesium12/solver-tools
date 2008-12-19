import itertools
from model.numbers import number_logprob
from model.language_model import english_model
from recognize import puzzle_logprob
known_transforms = []

def register_transform(f):
    known_transforms.append(f)
    return f

def apply_known_transforms(puzzle):
    next_steps = []
    for f in known_transforms:
        next_steps.extend(f(puzzle))
    return next_steps

@register_transform
def trans_map_trans(puzzle):
    next_steps = []
    if isinstance(puzzle, list) and len(puzzle) > 1:
        for f in known_transforms:
            x = map(f,puzzle)
            if len(x) < 1:
                continue
            if any([len(q) == 0 for q in x]):
                continue
            x = [q[0] for q in x]
            ps = [a for (a,b) in x]
            ys = [b for (a,b) in x]
            next_steps.append((ps[0], ys))
    return next_steps
            
import transforms

def a_star(initial_puzzle):
    initial_estimate = puzzle_logprob(initial_puzzle)
    queue = [(initial_estimate, 0.0, (initial_puzzle,), ())]
    extended = []
    while queue:
        estimated_cost, actual_cost, path, steps = heappop(queue)
        puzzle = path[-1]
        if puzzle in extended: continue
        extended.append(puzzle)
        yield cost, path, steps

        # TODO: interleave these better
        for transform in known_transforms:
            for nextcost, next, step in transform(puzzle):
                estimate = puzzle_logprob(next)
                heappush(queue, (actual_cost+nextcost+estimate,
                                 actual_cost+nextcost,
                                 path+(next,),
                                 steps+(step,)))

