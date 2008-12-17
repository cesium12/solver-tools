known_transforms = []


def register_transform(f):
    print "moo"
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
