from solvertools.lib.print_grid import array_to_string
import numpy as np

class Header(object):
    """
    An object to designate that something is a header, and not puzzle data
    to be operated on.
    """
    def __init__(self, text):
        if isinstance(text, Header):
            text = text.text
        self.text = text

    def __str__(self):
        return '__%s__' % self.text

    def __repr__(self):
        return 'Header(%r)' % self.text

class PuzzleArray(np.ndarray):
    """
    A class designed to hold a grid of stuff, mostly strings.
    The first row can be marked as a header.
    """
    def __new__(cls, data, copy=False):
        arr = np.array(data, dtype=object, copy=copy).view(cls)
        return arr
    
    def _one_line_repr(self):
        if type(self[0]) == PuzzleArray:
            return repr([row._one_line_repr() for row in self])
        else:
            return repr(list(self))

    def __repr__(self):
        if self.ndim == 0:
            # hate it when this happens
            return repr(self[()])
        if type(self[0]) == PuzzleArray:
            reprs = [row._one_line_repr() for row in self]
            formatted = ',\n\t'.join(reprs)
            return 'PuzzleArray([\n\t' + formatted + '\n])'
        else:
            return 'PuzzleArray(%r)' % list(self)

    def __str__(self):
        return array_to_string(self)

if __name__ == '__main__':
    puz = PuzzleArray([
        [Header('order'), Header('day'), Header('element')],
        [1, 'Sunday', 'sun'],
        [2, 'Monday', 'moon'],
        [3, 'Tuesday', 'fire'],
        [4, 'Wednesday', 'water'],
        [5, 'Thursday', 'wood'],
        [6, 'Friday', 'metal'],
        [7, 'Saturday', 'earth']
    ])
    print puz
