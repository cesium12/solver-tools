"""
Implements various WordNet-related operations.

Requires nltk.corpus.wordnet to be available.
"""
from nltk.corpus import wordnet as wn

def morphy_roots(word, include_self=False):
    """
    Determine a set of words that may be a root of the given word, based on
    WordNet's Morphy algorithm.

    By the nature of Morphy, this will only return words that are entries in
    WordNet. Set `include_self` to True if you want to get back the original
    word if it is itself in WordNet.

    In the vast majority of cases, this returns 0 or 1 results, but ambiguous
    words may return 2.

        >>> morphy_roots('rung')
        set(['RING'])
        >>> morphy_roots('rungs')
        set(['RUNG'])
        >>> morphy_roots('programmes')
        set(['PROGRAM', 'PROGRAMME'])
        >>> morphy_roots('rainbow cactuses')
        set(['RAINBOW CACTUS'])
        >>> morphy_roots('burninated')
        set([])
    """
    wnword = word.lower().replace(' ', '_')
    lemmas = set()
    for pos in 'vna':
        lemma = wn.morphy(wnword, pos)
        if lemma is not None and (include_self or lemma != wnword):
            lemmas.add(lemma.replace('_', ' ').upper())
    return lemmas


