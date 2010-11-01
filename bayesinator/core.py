"""The module defining the core Baysinator system."""

__all__ = ['puzzle_property','entropy_function','transformation','Puzzle','Solution','Transform','solve']

import heapq
import math


# A list of properties with no prerequisites.
_initial_properties = []


# An error message to print if someone seems to have used a decorator generator as a decorator.
_dec_gen_error_msg = 'Decorator generator argument is not a puzzle property. Did you forget to add () after the name of the decorator generator?'


def puzzle_property(*prereqs):
    """Returns a decorator for defining a property with given prerequisites.

    The decorator generator takes any number of arguments.  Each
    argument is a prerequisite and should be either a type or another
    property.  The decorator it returns can then be applied to a
    predicate function and the predicate will be installed in the
    puzzle property system.  The system will automatically test the
    predicate on all puzzle data which satisfy the prerequisites.  The
    property system will never automatically call the predicate on
    puzzle data which do not satisfy the prerequisites, so the
    prerequisites may be assumed as preconditions of the predicate
    function (at least when it is called by the property system).
    """

    # Try to throw a useful error if we were mistakenly called on a
    # function rather than on a list of prerequisites.
    for prereq in prereqs:
        if not isinstance(prereq, type):
            assert '_prereqs' in prereq.__dict__, _dec_gen_error_msg
            assert '_infers'  in prereq.__dict__, _dec_gen_error_msg

    # This is the actual decorator.
    def add_prereqs(f):
        """A puzzle property decorator for a given list of prerequisites."""

        # Bad stuff happens if we double-apply the decorator, so let's
        # check that the decorator hasn't already been applied and
        # that we're not (for some strange reason) overwriting
        # pre-existing data.
        assert '_prereqs' not in f.__dict__
        assert '_infers'  not in f.__dict__

        f._prereqs = prereqs
        f._infers  = []

        initial = True
        # Add a reference to this property to all of its prereqs, so
        # that they will be able to invoke the evaluation of this
        # property when they are found to be true.
        for prereq in prereqs:
            if not isinstance(prereq, type):
                prereq._infers.append(f)
                initial = False

        if initial:
            _initial_properties.append(f)

        return f

    return add_prereqs


def _make_puzzle_function(combiner):
    """Constructs a function which may have different versions for different puzzle types."""

    versions = []

    def decorator_gen(*prereqs):
        """A puzzle function decorator generator."""

        # Try to throw a useful error if we were mistakenly called on
        # a function rather than on a list of prerequisites.
        for prereq in prereqs:
            if not isinstance(prereq, type):
                assert '_prereqs' in prereq.__dict__, _dec_gen_error_msg
                assert '_infers'  in prereq.__dict__, _dec_gen_error_msg
        def version_decorator(f):
            """A puzzle function decorator for a given list of prerequisites."""
            assert '_prereqs' not in f.__dict__
            f._prereqs = prereqs
            versions.append(f)
            return f
        return version_decorator

    def funct(puzzle, *args, **kw_args):
        """A puzzle function."""
        vals = []
        for f in versions:
            satisfying = True
            for prereq in f._prereqs:
                if isinstance(prereq, type):
                    if not isinstance(puzzle.data, prereq):
                        satisfying = False
                        break
                else:
                    if not prereq in puzzle.props:
                        satisfying = False
                        break
            if satisfying:
                vals.append((f(puzzle.data, *args, **kw_args),f))

        return combiner(puzzle, vals)
        
    return (decorator_gen, funct)


def _entropy_combiner(puzzle, entropies):
    best_f = None
    best_e = float('inf')
    for (e,f) in entropies:
        if best_e > e:
            best_f = f
            best_e = e
    return (best_e, best_f)


def _transform_combiner(puzzle, transform_lists):
    transforms = []
    for (ts,f) in transform_lists:
        if not isinstance(ts, list):
            ts = [ts]
        for t in ts:
            if not isinstance(t, Transform):
                t = Transform(t)
            t.transformation = f
            t.source = puzzle
            transforms.append(t)
    return transforms




(entropy_function, _entropy) = _make_puzzle_function(_entropy_combiner)
(transformation, _transform) = _make_puzzle_function(_transform_combiner)
entropy_function.__name__ = 'entropy_function'
transformation.__name__ = 'transformation'


def get_method_entropy(puzzle, method):
    """Determine how likely we believe a method is to be the next step in solving a puzzle."""
    return math.log(10,2) # TODO: Improve on this


class Transform:

    """A structure holding the data for a single transform of a puzzle."""

    def __init__(self, puzzle_data, entropy=0.0, transform_data=None):
        """Create a new representation of a transform.
        
        Arguments:

        ``puzzle_data``
           Arbitrary data representing a new puzzle.

        ``entropy``
           This entropy is the sum of two things: the entropy of the
           choices made by the transformation in outputting the
           current puzzle data, and the entropy of the information in
           the original puzzle data which is *not* preserved in the
           new puzzle data.  Basically, this is how much information
           you would need to go backwards and construct the puzzle
           given the partly solved version if I told you the mechanism
           but not the specifics.  If the transformation is
           deterministic and invertable, then this value should be
           zero.

        ``transform_data``
           Any data the transformation wishes to include representing
           what choices in made in making this particular transform.
           If the transformation is deterministic, this can safely be
           set to None.

        """
        self.puzzle_data    = puzzle_data
        self.transform_data = transform_data
        self.entropy        = entropy
        # ``self.transformation`` will be set later by _transform_combiner
        # ``self.source`` will be set later by _transform_combiner


class Puzzle:

    """A class maintaining puzzle data with associated properties."""

    def __init__(self, data):
        """Create a new puzzle object from arbitrary data."""
        self.data = data
        self.props = set()

        # Check initial properties
        stack = []
        for prop in _initial_properties:
            type_check = True
            for t in prop._prereqs:
                if not isinstance(self.data, t):
                    type_check = False
                    break
            if type_check and prop(data):
                self.props.add(prop)
                stack.append(prop)
        # Search the property graph using DFS to find all satisfied
        # properties
        while len(stack) > 0:
            new_prop = stack.pop()
            for prop in new_prop._infers:
                satisfying = True
                for prereq in prop._prereqs:
                    if isinstance(prereq, type):
                        if not isinstance(self.data, prereq):
                            satisfying = False
                            break
                    else:
                        if not prereq in self.props:
                            # The puzzle may still satisfy the prereq,
                            # but we'll come back to the current
                            # property when we discover that.
                            satisfying = False
                            break
                if satisfying and prop(data):
                    self.props.add(prop)
                    stack.append(prop)

        # Calculate our entropy
        (self.entropy, self.entropy_function) = _entropy(self)

    def __cmp__(self, other):
        x = cmp(self.entropy, other.entropy)
        if x != 0:
            return x
        else:
            return cmp(self.data, other.data)


class Solution:

    """A (partial) solution to a puzzle.

    A solution comprises a final puzzle state, the original puzzle
    state, and a particular sequence of transformations which produce
    the final state from the original state.
    """

    def __init__(self, state, last=None, transform=None):
        if not isinstance(state, Puzzle):
            state = Puzzle(state)

        self.state     = state
        self.last      = last
        self.transform = transform

        assert (last is None) == (transform is None)

        # Calculate all the entropies for this solution
        self.state_entropy = state.entropy
        if last is None:
            self.path_entropy = 0
        else:
            self.path_entropy  = last.path_entropy + transform.entropy
            self.path_entropy += get_method_entropy(state, transform.transformation)
        self.entropy = self.path_entropy + self.state_entropy

    def __cmp__(self, other):
        x = cmp(self.entropy, other.entropy)
        if x != 0:
            return x
        x = cmp(self.state, other.state)
        if x != 0:
            return x
        x = cmp(self.last, other.last)
        return x


def solve(start):
    """Return a generator for an A* search for a solution."""
    if isinstance(start, Solution):
        pass
    elif isinstance(start, Puzzle):
        start = Solution(start)
    else:
        start = Solution(Puzzle(start))

    heap = []
    heapq.heappush(heap, start)

    while len(heap) > 0:
        partial = heapq.heappop(heap)
        yield partial
        for transform in _transform(partial.state):
            next = Solution(transform.puzzle_data, partial, transform)
            heapq.heappush(heap, next)
