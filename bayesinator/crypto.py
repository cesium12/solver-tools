from bayesinator.core import *


@transformation(str)
def rot13(s):
    t = []
    for c in s:
        if 'a' <= c <= 'z':
            t.append(chr(ord('a') + ((ord(c) - ord('a') + 13) % 26)))
        elif 'A' <= c <= 'Z':
            t.append(chr(ord('A') + ((ord(c) - ord('A') + 13) % 26)))
        else:
            t.append(c)
    return Transform(''.join(t))
