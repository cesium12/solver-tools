Mixmaster is an anagrammer. So far it doesn't use any particularly clever
search algorithms, it just chugs through a *whole lot* of data.

And, in fact, more data makes better anagrams. It knows what words and phrases
people actually use. If you ask something else such as oneacross.com to anagram
"high ninja block move", it will tell you meaningless things like "COMBLIKE
HAVING JOHN" and "OH BELCH INVOKING JAM".

If you ask Mixmaster:

    >>> from solvertools.anagram.mixmaster import *
    >>> simple_anagram('high ninja block move')
    ('BEING JOHN MALKOVICH', 117719)

The key ideas of Mixmaster:

- Precompute everything possible.
- Consume as much data as possible.

So, given a reasonable-length text, Mixmaster searches for how to anagram it
into one or two phrases in the Puzzlebase (whose anagrams are precomputed). Two
phrases doesn't sound like a lot, but you can make a whole lot out of two
phrases in the Puzzlebase.

The documentation at the function level is a bit sparse right now -- sorry.

.. automodule:: solvertools.anagram.mixmaster
   :members:

