from regex import is_regex, regex_index, regex_sequence, UNKNOWN, INVALID
from solvertools.lib.print_grid import array_to_string
from solvertools.wordlist import alphanumeric_only
import numpy as np
import string
import codecs

class PuzzleArray(np.ndarray):
    """
    A class designed to hold a grid of stuff, particularly strings,
    and FlagValues.
    """
    def __new__(cls, data, copy=False):
        arr = np.array(data, dtype=object, copy=copy).view(cls)
        return arr

    # Example: test2="order\tlength\tday\telement\n1\t6\tSunday\tsun\tsun\n2\t6\tMonday\tmoon\tmoon\n3\t7\tTuesday\tfire\tTiu\n4\t9\tWednesday\twater\tWoden\n5\t8\tThursday\twood\tThor\n6\t6\tFriday\n7\t8\t\tearth\tSaturn", run tabsep_array_to_lists(test2)
    # Expects text '\t' and '\n' delimited, pads the header column with '__Col <n>__' and missing data/short lines with '/.*/'
    @staticmethod
    def from_tabular(text):
        """
        Create a PuzzleArray from tabular data, provided as a string.
        """
        def element_transform(elt):
            if elt == '':
                return '/.*/'
            elif len(elt) > 4 and elt.startswith('__') and elt.endswith('__'):
                return Header(elt[2:-2])
            else:
                return elt

        out_list=[]
        lines=text.split('\n')

        for line in rest_lines:
            line_transform=[element_transform(elt) for elt in line.split('\t')]
            out_list.append(line_transform)

        max_cols=max(len(line) for line in out_list)

        for line in out_list:
            if len(line)<max_cols:
                line.extend(['/.*/']*(max_cols-len(line)))
        return out_list

    @staticmethod
    def load(filename):
        """
        Loads tabular data from a file. The file should contain UTF-8
        tab-separated values.
        """
        file = codecs.open(filename, encoding='utf-8', errors='replace')
        table = PuzzleArray.from_tabular(file.read().strip())
        file.close()
        return table

    def save(self, filename):
        file = codecs.open(filename, 'w', encoding='utf-8', errors='replace')
        table = PuzzleArray.from_tabular(file.read().strip())
        file.close()
    
    def column(self, title):
        """
        Get the column containing a given header or with a given 0-based
        index, or raise a KeyError if it's not there.

        This does not use any sort of efficient index.
        """
        if isinstance(title, int):
            return self[:, title]

        header = Header(title)
        for col in xrange(self.shape[1]):
            if header in list(self[:, col]):
                return self[:, col]

    def column_title(self, index):
        """
        Get the header of the column with a given index, or just the index
        as a string if it has no header.
        """
        for item in self[:, index]:
            if isinstance(item, Header):
                return item.text
        return u'column '+unicode(index)

    def _one_line_repr(self):
        if type(self[0]) == PuzzleArray:
            return repr([row._one_line_repr() for row in self])
        else:
            return repr(list(self))

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
    
    def to_string(self):
        assert self.ndim == 1
        return regex_sequence([unicode(item) for item in self
                               if not isinstance(item, Header)])

    def index_everything_into_everything(self):
        from solvertools.model.language_model import get_english_model
        model = get_english_model()

        assert self.ndim == 2
        ncol = self.shape[1]
        titles = [self.column_title(idx) for idx in xrange(ncol)]
        results = []

        def evaluate(indexed, description):
            if INVALID not in indexed:
                text = indexed.to_string()
                length = len(text)
                spaced_text, prob = model.split_words(text)
                goodness = prob/length
                results.append((description, spaced_text, goodness))
        
        def try_sorted(sorted, sort_title):
            for text_col in xrange(ncol):
                text_title = titles[text_col]
                for index_col in xrange(ncol):
                    index_title = titles[index_col]
                    description = u"%s%s[%s]" %\
                      (sort_title, text_title, index_title)
                    
                    indexed = index_lists(sorted[:,text_col],
                                          sorted[:,index_col])
                    evaluate(indexed, description)

                # also try diagonalizing
                description = u"%s%s[1]" %\
                  (sort_title, text_title)
                indexed = index_lists(sorted[:, text_col],
                                      np.ones(len(sorted)))
                evaluate(indexed, description)
                
                # also try diagonalizing
                description = u"%s%s[diag]" %\
                  (sort_title, text_title)
                indexed = sorted[:, text_col].diagonalize()
                evaluate(indexed, description)

        for sort_col in xrange(ncol):
            sorted = self.sort_by(sort_col)
            sort_title = titles[sort_col] + ':'
            try_sorted(sorted, sort_title)
            try_sorted(sorted[::-1], '-'+sort_title)
        try_sorted(self, '')
        try_sorted(self[::-1], '-')

        results.sort(key=lambda item: -item[2])
        result_headers = (Header('operation'), Header('text'),
                          Header('goodness'))
        return PuzzleArray([result_headers] + results)
    
    def diagonalize(self):
        assert self.ndim == 1
        values = [item for item in self if not isinstance(item, Header)]
        indices = np.arange(len(values)) + 1
        return index_lists(values, indices)

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
            return array_to_string(self, height=25)
        elif self.ndim == 1:
            return array_to_string(self[:,np.newaxis], height=25)
        else: return repr(self)

class FlagValue(object):
    """
    The parent class of entries that aren't supposed to be literal
    values, but are supposed to flag that something else is going on.
    """
    def __str__(self):
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        raise NotImplementedError

    def __hash__(self):
        return hash(unicode(self))

    def __cmp__(self, other):
        return cmp((str(type(self)), unicode(self)),
                   (str(type(other)), unicode(other)))
    
    def __getitem__(self, index):
        return INVALID

class Header(FlagValue):
    """
    An object to designate that a table entry is a header, and not puzzle data
    to be operated on.
    """
    def __init__(self, text):
        if isinstance(text, Header):
            text = text.text
        self.text = text

    def __repr__(self):
        return 'Header(%r)' % (self.text,)

    def __str__(self):
        return unicode(self).encode('utf-8')
    
    def __unicode__(self):
        return u'__%s__' % (self.text,)
    
    def __getitem__(self, other):
        if isinstance(other, Header):
            other = other.text
        return Header(u'%s[%s]' % (self.text, other))

def regex_or_convert(seq, converter=alphanumeric_only):
    """
    Apply a text conversion to a given string, unless it's actually a
    FlagValue or a regex, in which case leave it alone.
    """
    if isinstance(seq, FlagValue):
        return seq
    elif is_regex(seq):
        return seq
    else:
        return converter(seq)

def is_numeric(text):
    try:
        return (unicode(int(text)) == text)
    except ValueError:
        return False

def index_into(text, index, numbers_are_okay=False):
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
                    text = regex_or_convert(text, alphanumeric_only)
                    index = int(index)
                    if is_numeric(text) and not numbers_are_okay:
                        return INVALID
                    if index < 1:
                        return INVALID
                    else:
                        return regex_index(text, index-1)
                except (TypeError, IndexError, ValueError):
                    return INVALID
    else:
        return INVALID

def index_lists(list1, list2):
    return PuzzleArray([index_into(text, index)
                        for text, index in zip(list1, list2)])

if __name__ == '__main__':
    puz = PuzzleArray([
        [Header('order'), Header('length'), Header('day'), Header('element'), Header('god')],
        [1, 6, 'Sunday', 'sun', 'sun'],
        [2, 6, 'Monday', 'moon', 'moon'],
        [3, 7, 'Tuesday', 'fire', 'Tiu'],
        [4, 9, 'Wednesday', 'water', 'Woden'],
        [5, 8, 'Thursday', 'wood', 'Thor'],
        [6, 6, 'Friday', 'metal', 'Freya'],
        [7, 8, 'Saturday', 'earth', 'Saturn']
    ])

    puz2 = PuzzleArray([
        [Header('Puzzle'), Header('Flavortext word'),
         Header('Matching answer'), Header('Answer number'),
         Header('Matching puzzle')],
        "Meta, venerated, HOLY TRINITY, 3, Too Much Clue".split(', '),
        "Too Much Clue, series, STRING QUARTET, 4, Left Out".split(', '),
        "Left Out, stoned, HIGH PAIR, 2, \\varphi".split(', '),
        "\\varphi, circadian, DAILY DOUBLE, 2, Lego My Ego".split(', '),
        "Lego My Ego, tense, STRAINED QUAD, 4, Silly Hat Brigade".split(', '),
        "Silly Hat Brigade, strike, HIT SINGLE, 1, TCNMAAWATT".split(', '),
        "TCNMAAWATT, lessened, DIMINISHED TRIAD, 3, Piranhas in a Bathtub".split(', '),
        "Piranhas in a Bathtub, leave, SPLIT SECOND, 2, IIF".split(', '),
        "IIF, relish, LOVE TRIANGLE, 3, Lake Effect Snow".split(', '),
        "Lake Effect Snow, brotherly, FRATERNAL TWINS, 2, Setec Astronomy"\
        .split(', ')
    ])
    print [len(row) for row in puz2]
    print puz2
    print puz2.index_everything_into_everything()
