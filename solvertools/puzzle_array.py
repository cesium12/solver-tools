from values import alphanumeric_filter, PuzzleString, Header, FlagValue, \
                   ChoiceValue, UNKNOWN, INVALID

from solvertools.lib.print_grid import array_to_string
import numpy as np

class PuzzleArray(np.ndarray):
    """
    A class designed to hold a grid of stuff, particularly strings,
    PuzzleStrings, and FlagValues.
    """
    def __new__(cls, data, copy=False):
        arr = np.array(data, dtype=object, copy=copy).view(cls)
        return arr
    
    def column(self, title):
        """
        Get the column containing a given header, or raise a KeyError if it's
        not there.

        This does not use any sort of efficient index.
        """
        header = Header(title)
        for col in xrange(self.shape[1]):
            if header in list(self[:, col]):
                return self[:, col]

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
        if self.ndim == 2:
            return array_to_string(self)
        elif self.ndim == 1:
            return array_to_string(self[:,np.newaxis])
        else: return repr(self)

    def to_puzzle_string(self):
        if self.ndim > 1:
            return PuzzleArray([to_puzzle_string(row) for row in self])
        else:
            return PuzzleString([item for item in self
                                 if not isinstance(item, Header)])

    def sort_by(self, col):
        """
        Sort this puzzle according to one of its columns. The column can be
        specified as either a 0-based index, a header name, or the column of
        data to sort by itself.

        This tries to keep headers at the top.
        """
        if isinstance(col, int):
            col = self[:, col]
        elif isinstance(col, basestring):
            col = self.column(col)
        col = col.copy()
        for i, item in enumerate(col):
            if isinstance(item, Header):
                col[i] = None
        sort_order = np.argsort(col)
        return self[sort_order]

def index_into(text, index):
    """
    Gets the letter at a certain position in a text. Makes assumptions that are
    reasonable for puzzles:
 
    - Spaces and punctuation don't count.
    - Indices start at 1, not 0.
    - Indexing off the end of a text means you probably shouldn't be doing it.
    """
    if hasattr(text, '__getitem__'):
        if (not text) or text == ' ':
            # Empty values might indicate spaces.
            return ' '
        else:
            if isinstance(text, Header) and isinstance(index, Header):
                # headers index headers to make new headers
                return text[index]
            else:
                try:
                    text = alphanumeric_filter(text)
                    index = int(index)
                    if index < 1:
                        return INVALID
                    else:
                        return text[index-1]
                except (TypeError, IndexError, ValueError):
                    return INVALID
    else:
        return INVALID

def index_lists(list1, list2):
    return PuzzleArray([index_into(text, index)
                        for text, index in zip(list1, list2)])

if __name__ == '__main__':
    puz = PuzzleArray([
        [Header('order'), Header('length'), Header('day'), Header('element')],
        [1, 6, 'Sunday', 'sun'],
        [2, 6, 'Monday', 'moon'],
        [3, 7, 'Tuesday', 'fire'],
        [4, 9, 'Wednesday', 'water'],
        [5, 8, 'Thursday', 'wood'],
        [6, 6, 'Friday', 'metal'],
        [7, 7, 'Saturday', 'earth']
    ])
    print puz
    print index_lists(puz.column('day'), puz.column('order'))

