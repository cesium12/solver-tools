"""
`solvertools.puzzlebase.clue` takes in clues, and frequently answers them using
the Puzzlebase. It's like One Across, but probably better. It's trained on
various wordlists, interesting Google bigrams and trigrams, a corpus of
crossword puzzles including thousands from the New York Times, and WordNet.

This documentation will give a number of illustrative examples by asking
for a very small number of matches (1 or 3). Don't do that on real puzzles.
You might find the right answer much farther down the list. But here's an
example:

    >>> match_clue('marsupial', 5)
    [u'MARSUPIALOID', u'MARSUPIATE', u'MARSUPIAN', u'DASYURID', u'OPOSSUMRAT']

If you want to specify an answer length, it goes in parentheses at the end
of the clue. It has to be a single integer; it can't be separated into
different words, because the Puzzlebase is rather vague about word
boundaries anyway.

    >>> match_clue('Assertion of the falsity of a given proposition (8)', 3)
    [u'ARGUMENT', u'DISPROOF', u'CONTRARY']

Instead of a length, you can give a regex between slashes at the end of
the clue. If the regex is the entire clue, then this module will
hand the job off to Regulus to search the entire wordlist.

    >>> match_clue('United States President /.A....../', 3)
    [u'VANBUREN', u'GARFIELD', u'HARRISON']

    >>> match_clue('/.A.B.C../', 3)
    [u'BARBECUE', u'BARBICAN', u'TABBYCAT']

The solver prioritizes matching as many words as possible, making it good
for "what do these have in common?" clues:

    >>> match_clue('black union hi', 3)
    [u'JACK', u'CASUAL', u'BOSS']

    >>> match_clue('easy double new', 3)
    [u'DEADRINGER', u'TROUBLE', u'SPEAK']

    >>> match_clue('noise castle lie', 3)
    [u'WHITE', u'LIKE', u'BEAUTIFUL']

The intended answers were "JACK", "SPEAK", and "WHITE" respectively, but I can
see how "TROUBLE" gets in there.

Do not expect any deep insight from these answers! It's really just
matching words together and can be tripped up by simple paraphrases.
It's certainly not IBM's Watson.

Here's a clue that doesn't entirely work well, because it requires
understanding grammar and context:

    >>> match_clue('Who shot Abraham Lincoln? (15)', 1)
    [u'LINCOLNMEMORIAL']

The next answer is "STEPHENADOUGLAS", and then "PRESIDENTARTHUR". Even
"STEPHENSONDHEIM" rankes higher than "JOHNWILKESBOOTH", the 70th answer.

Using a more specific word will get a better result:

    >>> match_clue('Lincoln assassin (15)', 1)
    [u'JOHNWILKESBOOTH']

Let's conclude with a very silly example:

    >>> match_clue('(50)', 3)
    [u'THEOPHRASTUSPHILIPPUSAUREOLUSBOMBASTUSVONHOHENHEIM',
     u'AGECANNOTWITHERHERNORCUSTOMSTALEHERINFINITEVARIETY',
     u'ALLOVERTHEWORLDTHEVERYBESTOFELECTRICLIGHTORCHESTRA']
"""

from solvertools.regex import bare_regex
from solvertools.wordlist import alphanumeric_only, COMBINED
from solvertools.puzzlebase.mongo import DB, known_word
from solvertools.model.tokenize import tokenize
from math import log, exp
from collections import defaultdict
import re
import divisi2

MATRIX = divisi2.load('clues.rmat')
def associations(words, similarity_min=-1., beam=1000):
    """
    Find words associated with a set of words in the database. Use a few
    heuristics to find the most relevant results.
    """
    possibilities = set()
    minimum = similarity_min
    mapping = defaultdict(lambda: defaultdict(lambda: minimum))
    words = [alphanumeric_only(w) for w in words]
    word_freqs = {}
    for word in words:
        word_freqs[word] = COMBINED.get(word, 100)
        query = DB.associations.find({'source': word})
        query2 = DB.associations.find({'target': word})

        for match in list(query[:beam]) + list(query2[:beam]):
            word2 = match['target']
            if word2 == word:
                word2 = match['source']
            possibilities.add(word2)
            value = match.get('value')
            mapping[word2][word] = max(mapping[word2][word], value)

        if word in MATRIX.row_labels:
            for word2, value in MATRIX.row_named(word).top_items(beam):
                if value > 0:
                    value = value / 10
                    possibilities.add(word2)
                    mapping[word2][word] = max(mapping[word2][word], value)

    for word in words:
        for word2 in possibilities:
            matrix_entry = MATRIX.entry_named(word, word2) / 10
            mapping[word2][word] = max(mapping[word2][word], matrix_entry)

    results = {}
    for word2 in possibilities:
        results[word2] = sum([mapping[word2][word]/(word_freqs[word]**.5) for word in words])
    best_results = sorted(results.items(), key=lambda x: -x[1])
    return best_results

def match_words(words, pattern='.*', n=25, similarity_min=-1.):
    """
    Like :func:`associations`, but also takes in a pattern to match, and
    filters its results to only ones that match the pattern.
    """
    if isinstance(pattern, int):
        pattern = '.'*pattern
    if not words:
        return match_pattern(pattern, n)
    re_pattern = re.compile(bare_regex(pattern))
    matches = []
    used = set()
    for word, goodness in associations(words, similarity_min=similarity_min):
        match = re_pattern.match(word)
        if match and match.end() == len(word):
            matches.append((word, goodness))
            used.add(word)
            if len(matches) >= n:
                break
    return matches

def match_pattern(pattern, n=25):
    """
    In the case that we have no clue words to match, this hands off the job
    to Regulus, the high-speed wordlist grepper.
    """
    if pattern == '.*':
        raise ClueFormatError("I think you're asking me to iterate over the entire database. Sorry, no.")
    
    matches = COMBINED.grep(pattern)
    matches.sort(key=lambda x: -x[1])
    return [(unicode(match), freq) for match, freq in matches[:n]]

def extract_words(text):
    "Get just the words out of possibly-punctuated text."
    words = tokenize(text).split()
    return [alphanumeric_only(word) for word in words if alphanumeric_only(word)]

def extract_words_and_phrases(text, maxwords=4):
    """
    Extract words and reasonable-looking phrases from text.
    """
    words = extract_words(text)
    phrases = []
    for length in xrange(1, maxwords+1):
        for left in xrange(len(words)-length+1):
            right = left+length
            phrase = ''.join(words[left:right])
            if len(phrase) > 5 and phrase in COMBINED:
                phrases.append(phrase)
    return _filter_too_common(words+phrases)

def _filter_too_common(words, threshold=1000000000):
    """
    Filter words that are so common that they cannot meaningfully change the
    results. (These words would have their 'interestingness' multiplied by a
    very small number anyway; this just rounds that number off to 0.) 
    
        >>> _filter_too_common(['the', 'system', 'of', 'the', 'world'])
        ['system', 'world']

    This will return the original input instead of filtering out all words:
        
        >>> _filter_too_common(['to', 'be', 'or', 'not', 'to', 'be'])
        ['to', 'be', 'or', 'not', 'to', 'be']
    """
    result = [word for word in words if COMBINED.get(word, 100) <= threshold]
    if result:
        return result
    else:
        return words

class ClueFormatError(ValueError):
    pass

def match_clue(clue, n=25, similarity_min=-1.):
    """
    Takes in a clue using vaguely natural syntax, with a possible length or
    regular expression specified. Returns a list of the `n` best matches
    to the clue.

    See this module's documentation for a full description and examples.
    """
    clue = clue.strip()
    if clue.endswith('/'):
        try:
            clue_text, regex, _ = clue.rsplit('/', 2)
            clue_text = clue_text.strip()
        except ValueError:
            clue_text = clue
            regex = '.*'
    elif clue.endswith(')') and '(' in clue:
        clue_text, length = clue[:-1].rsplit('(', 1)
        clue_text = clue_text.strip()
        try:
            length = int(length)
        except ValueError:
            raise ClueFormatError("I don't understand (%s) as a length. Did you mean to use a /regular expression/?" % length)
        regex = '.'*length
    else:
        clue_text = clue
        regex = '.*'

    if ';' in clue_text:
        clue_words = [w.strip() for w in clue_text.split(';')]
    else:
        clue_words = extract_words_and_phrases(clue_text)
    return [got[0] for got in match_words(clue_words, pattern=regex, n=n, similarity_min=similarity_min)]

