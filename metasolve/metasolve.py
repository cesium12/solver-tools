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
    pattern = pattern.upper()

    def fits(trie, pat, partial_word):
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
            

    @memoize.Memoize
    def dp(pat, history):
        #print "dp(%s,%s)" % (pat, history)
        if not pat:
            return uncertain.Uncertain(lambda : iter([(0,[])]))
        options = []
        for (next, rest_pat) in fits(dict_trie, pat, ""):
            #print "(%s,%s)" % (next, rest_pat)
            opt = dp(rest_pat, lang_model.trim_context(history + [next]))
            opt.Shift(math.log(lang_model.prob(next, history)))
            it = iter([(w, [next]+rest) for (w,rest) in opt])
            options.append(uncertain.Uncertain((lambda x: lambda : x)(it)))
        print "fits(dict_trie, pat, '') = %s" % fits(dict_trie, pat, "")
        print [[x for x in y] for y in options]
        print [y for y in uncertain.Merge(options)]
        return uncertain.Merge(options)
            
    return dp(pattern, [])
