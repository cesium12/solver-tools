"""
Implements various WordNet-related operations.

Requires nltk.corpus.wordnet to be available.
"""
from nltk.corpus import wordnet as wn

def morphy_adverb(word):
    """
    Do the equivalent of Morphy for adverbs.

    >>> morphy_adverb('realistically')
    set(['REALISTIC'])
    >>> morphy_adverb('magically')
    set(['MAGIC', 'MAGICAL'])
    >>> morphy_adverb('happily')
    set(['HAPPY'])
    >>> morphy_adverb('frabjously')
    set([])
    """
    word = word.lower().replace(' ', '_')
    results = []
    if len(word) >= 8 and word.endswith('ally'):
        results.append(wn.morphy(word[:-4], 'a'))
    if len(word) >= 4 and word.endswith('ly'):
        results.append(wn.morphy(word[:-2], 'a'))
    if len(word) >= 6 and word.endswith('ily'):
        results.append(wn.morphy(word[:-3]+'y', 'a'))
    return set([r.replace('_', ' ').upper() for r in results if r is not None])

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
        >>> morphy_roots('was')
        set(['BE'])
        >>> morphy_adverb('magically')
        set(['MAGIC', 'MAGICAL'])
    """
    wnword = word.lower().replace(' ', '_')
    lemmas = set()
    if include_self:
        lemmas.add(word)
    for pos in 'vna':
        lemma = wn.morphy(wnword, pos)
        if lemma is not None and (include_self or lemma != wnword):
            lemmas.add(lemma.replace('_', ' ').upper())
    
    # special cases
    if wnword == 'was':
        lemmas.remove('WA')
    elif wnword == 'has':
        lemmas.remove('HA')
    return lemmas | morphy_adverb(word)

