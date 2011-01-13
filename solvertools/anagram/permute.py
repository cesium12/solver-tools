def number_of_swaps(permutation):
    """Find number of swaps required to convert the permutation into
    identity one.
    """
    # decompose the permutation into disjoint cycles
    nswaps = 0
    seen = set()
    for i in xrange(len(permutation)):
        if i not in seen:           
           j = i # begin new cycle that starts with `i`
           while permutation[j] != i:
               j = permutation[j]
               seen.add(j)
               nswaps += 1

    return nswaps

def anagram_to_permutation(original, anagrammed):
    letterbank = list(original)
    indices = []
    for char in anagrammed:
        try:
            index = letterbank.index(char)
        except ValueError:
            raise ValueError("The inputs must be anagrams of each other")
        indices.append(index)
        letterbank[index] = None
    return indices

def swap_distance(original, anagrammed):
    """
    Get the minimum number of letter pairs that need to be swapped to turn
    one string into another. (This will raise a ValueError if the strings
    are not in fact anagrams of each other).

    A higher swap distance gives a more appealing, less obvious anagram.

        >>> swap_distance('BEINGJOHNMALKOVICH', 'HIGHNINJABLOCKMOVE')
        15
        >>> swap_distance('BEINGJOHNMALKOVICH', 'BEGINJOHNMALKOVICH')
        2
    """
    return number_of_swaps(anagram_to_permutation(original, anagrammed))
