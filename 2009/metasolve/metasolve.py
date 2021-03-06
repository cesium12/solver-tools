# Copyright (c) 2008, Alex Schwendner
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
# 
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above
#       copyright notice, this list of conditions and the following
#       disclaimer in the documentation and/or other materials
#       provided with the distribution.
#     * Neither the name of the Manic Sages nor the names of its
#       contributors may be used to endorse or promote products
#       derived from this software without specific prior written
#       permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

__author__ = 'alexrs@csail.mit.edu (Alex Schwendner)'


import math
import operator

import memoize
import trie
import uncertain


def metasolve(pattern, dict_trie, lang_model):
    """Returns a lazy list of possible metapuzzle answers.

    Args:

      pattern: a string with the letters known and '?' as a wildcard

      dict_trie: a trie containing all words

      lang_model: a language model implementing the
        trim_context(history) and prob(next, history) methods.
        prob(next, history) should return a real number in the range
        [0,1] for the estimated probability of the next word being
        'next' given the preceeding words contained in the list
        'history'. trim_context(history) takes a list of preceeding
        words and returns a (hopefully shorter) suffix which yields
        the same probability distributions.

    Returns: an instance of Uncertain containing (log-probability,
      word sequence) pairs sorted in decending order of probability.
    """
    pattern = pattern.upper()

    def fits(trie, pat, partial_word):
        """Returns a list of words which might fit next in a pattern.

        Args:

          trie: a dictionary trie

          pat: a pattern string using '?' as a wildcard

          partial_word: the word prefix already matched
        """
        options = []
        if trie.value:
            options.append((partial_word, pat))
        if not pat:
            return options
        if pat[0] == '?':
            return reduce(operator.concat,
                          [fits(trie.next_dict[c],
                                pat[1:],
                                partial_word + c)
                           for c in trie.next_dict.keys()],
                          options)
        elif pat[0] in trie.next_dict:
            return options + fits(trie.next_dict[pat[0]],
                                  pat[1:],
                                  partial_word + pat[0])
        else:
            return options

    def PrependWordAndShift(g, dw, next):
        for (w,rest) in g:
            yield (w+dw, [next]+rest)

    @memoize.Memoize
    def dp(pat, history):
        if not pat:
            return uncertain.Uncertain([(0,[])])
        options = []
        q = fits(dict_trie, pat, "")
        for (next, rest_pat) in q:
            opt = dp(rest_pat, lang_model.trim_context(history + [next]))
            dw = math.log(lang_model.prob(next, history))
            options.append(uncertain.Uncertain(PrependWordAndShift(opt, dw, next)))
        return uncertain.Merge(options)
            
    return dp(pattern, [])
