from regex import is_regex, regex_index, regex_sequence, INVALID
from solvertools.lib.print_grid import array_to_string
from solvertools.wordlist import alphanumeric_only
import numpy as np
import string
import codecs
import csv

def numeric_sort_key(s):
    try:
        return float(s)
    except ValueError:
        return s

class PuzzleArray(np.ndarray):
    """
    A class designed to hold a grid of stuff, particularly strings. Very
    useful for storing a partially-completed puzzle.

    Here's an example of using it on the 2009 puzzle "Soylent Partners":

        >>> from solvertools.util import get_datafile
        >>> puz = PuzzleArray.load(get_datafile('test/soylent_partners.csv'))
        >>> print puz
        __order__ __color__ __colorna __clue_a_ __person_ __clue_b_ __person_ ...
        1         800000    Maroon    Tony who  Soprano   Tony who' Romo     
        2         00FFFF    Cyan      Travis of McCoy     Ted who o Danson   
        3         272974    Navy      Eva who s Mendes    singer bo Vanity   
        4         FF7F00    Orange    Rod who h Serling   Daniel, p Ortega   
        5         DC143C    Crimson   Robert wh MacNeil   Johnny wh Storm    
        6         FF7F50    Coral     Stephen o Colbert   Bobby, a  Seale    
        7         FF00FF    Magenta   George wh eastman   Rufus who King     
        8         D2B48C    Tan       Dean know Cain      Tony, a d baretta  
        9         FFBF00    Amber     Andy, the samberg   Hunt or T sales    
        10        0000FF    Blue      Stephan o Lebeau    Sonny who liston   
        11        FDE910    Lemon     Eric, a f Clapton   Rosalind  miles    
        12        FF2400    Scarlet   Jacques w cartier   Mort, a s sahl     
        13        FFFF00    Yellow    Derek who Lowe      Anne who  Boleyn   
        14        B57EDC    Lavender  James, a  Carville  Anthony,  Eden     
        15        DE3163    Cerise    Maurits,  Escher    Bret who  ellis    
        
        >>> puz.try_indexing(1)
        Best answer
        ===========
        Operation: column_order:colorname[inspector]
        Extracted text: RAINBOWCACTUSES
        Suggested answer: RAINBOW CACTUSES
        Goodness: -3.479
        u'RAINBOW CACTUSES'

    PuzzleArrays are also great at working with unknown or partially known
    strings:
    
        >>> from solvertools.util import get_datafile
        >>> puz = PuzzleArray.from_csv(get_datafile('test/soylent_incomplete.csv'))
        >>> print puz
        __order__ __color__ __colorna __clue_a_ __person_ __clue_b_ __person_ ...
        1         800000    /.*/      Tony who  Soprano   Tony who' Romo     
        2         00FFFF    Cyan      Travis of McCoy     Ted who o Danson   
        3         272974    /.*/      Eva who s Mendes    singer bo Vanity   
        4         FF7F00    Orange    Rod who h Serling   Daniel, p Ortega   
        5         DC143C    /.*/      Robert wh MacNeil   Johnny wh Storm    
        6         FF7F50    Coral     Stephen o Colbert   Bobby, a  Seale    
        7         FF00FF    Magenta   George wh eastman   Rufus who King     
        8         D2B48C    /.*/      Dean know Cain      Tony, a d baretta  
        9         FFBF00    Amber     Andy, the samberg   Hunt or T sales    
        10        0000FF    Blue      Stephan o Lebeau    Sonny who liston   
        11        FDE910    Lemon     Eric, a f Clapton   Rosalind  miles    
        12        FF2400    /S.+/     Jacques w cartier   Mort, a s sahl     
        13        FFFF00    /Yello./  Derek who Lowe      Anne who  Boleyn   
        14        B57EDC    /.*/      James, a  Carville  Anthony,  Eden     
        15        DE3163    /.*/      Maurits,  Escher    Bret who  ellis    
       
        >>> puz.try_indexing(1)
        Best answer
        ===========
        Operation: column_order:colorname[inspector]
        Extracted text: /...NBO.CAC.US../
        Suggested answer: RAINBOW CACTUS OF
        Goodness: -2.649
        u'RAINBOW CACTUS OF'
    """
    def __new__(cls, data, copy=False):
        arr = np.array(data, dtype=object, copy=copy).view(cls)
        return arr

    @staticmethod
    def from_csv(filename, has_header=None):
        """
        Creates a PuzzleArray from any .csv file that Python's csv module
        can handle. If it detects a header row (or is told to use one),
        the first row will be converted to PuzzleArray headers.
        """
        fin = codecs.open(filename, 'rb')

        # Try to guess the format of the CSV file
        sample = fin.read(1024)
        dialect = csv.Sniffer().sniff(sample)
        if has_header is None:
            has_header = csv.Sniffer().has_header(sample)
        fin.seek(0)

        reader = csv.reader(fin, dialect)
        lines = iter(reader)
        rows = []
        if has_header:
            header_row = lines.next()
            rows.append([Header(unicode(text, 'utf-8')) for text in header_row])
        for row in lines:
            rows.append([unicode(text, 'utf-8') if text else "/.*/"
                         for text in row])
        fin.close()
        return PuzzleArray(rows)
    
    load = from_csv

    def save(self, filename):
        file = codecs.open(filename, 'w', encoding='utf-8', errors='replace')
        
        raise NotImplementedError # TODO
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
            else:
                col[i] = numeric_sort_key(item)
        sort_order = np.argsort(col)
        return self[sort_order]
    
    def to_string(self):
        assert self.ndim == 1
        return regex_sequence([unicode(item) for item in self
                               if not isinstance(item, Header)])

    def index_everything_into_everything(self):
        """
        Try indexing every column into every other column that's possible,
        sorting the resulting letters by every column as well. This method
        is sometimes all you need to get a puzzle from stuck to unstuck.

        Returns a new PuzzleArray with four columns:

        - operation: a concise representation of what you need to do to get
          this result. If the result is "sortby:text[indexby]", that means
          to sort by the 'sortby' column, and index the 'text' column by the
          'indexby' column.
        """
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
                results.append((description, text, spaced_text, goodness))
        
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

        results.sort(key=lambda item: -item[3])
        result_headers = (Header('operation'), Header('text'),
                          Header('best answer'), Header('goodness'))
        return PuzzleArray([result_headers] + results)

    def try_indexing(self, n=3):
        """
        Print the results of :meth:`index_everything_into_everything` in
        a human-readable form.
        """
        indexed = self.index_everything_into_everything()
        for i in xrange(1, n+1):
            op, text, answer, goodness = indexed[i]
            if i == 1:
                print "Best answer"
                print "==========="
            else:
                print
                print "Answer #%d" % i
                print "========="
            print "Operation:", op
            print "Extracted text:", text
            print "Suggested answer:", answer
            print "Goodness: %3.3f" % (goodness,)
        # return the best answer
        return indexed[1, 2]


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
        if text is None or text == '' or text == ' ':
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
                        for text, index in zip(list1, list2)
                        if not isinstance(text, Header)])

if __name__ == '__main__':
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
