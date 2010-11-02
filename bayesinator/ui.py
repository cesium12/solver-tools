from bayesinator.core import *


def show_solution(state):
    depth = 0
    p = state
    while p.last is not None:
        depth += 1
        p = p.last

    ss = []
    ss.append(str(state.entropy))
    ss.append("  (%d) %r (%f)" % (depth, state.state.data, state.state_entropy))
    while state.last is not None:
        t = state.transform
        f = t.transformation
        ss.append("   ^  %s.%s[%r] (%f)" % (f.__module__, f.__name__, t.transform_data, t.entropy))
        depth -= 1
        state = state.last
        ss.append("  (%d) %r (%f)" % (depth, state.state.data, state.state_entropy))

    return '\n'.join(ss)


def main():
    while True:
        print "Enter puzzle (as a Python object):"
        puzzle = input()
        print "How many iterations?"
        n = int(raw_input())
        ss = solve(puzzle)
        for i in range(n):
            print show_solution(ss.next())
            print
