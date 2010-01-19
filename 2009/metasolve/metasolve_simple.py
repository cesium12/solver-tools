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


from metasolve import metasolve
import model_freq
import trie
from sagesutil import export


model = None
dict_trie = None

@export(description="""A simple interface to the metapuzzle solver. Takes a pattern for the metapuzzle answer, with known letters mized with '?' used as a wildcard, and outputs the most likely completions.""",
  args=["The pattern", "The desired number or results"],
  ret="A sorted list of possible completions, each of which is a pair (log-probability, list of answer words).")
def metasolve_simple(pattern, hits):
    global model
    global dict_trie
    if not model:
        model = model_freq.FreqModel()
        print "Reading file..."
        model.readBNC("metasolve/bnc.all.al.gz")
        print "DONE"
    if not dict_trie:
        print "Building dict trie..."
        dict_trie = trie.Trie()
        for word in model.all_words():
            dict_trie.insert(word)
        print "DONE"

    ans = []
    for (w,v) in metasolve(pattern, dict_trie, model):
        ans.append((w,v))
        if len(ans) >= hits:
            break

    return ans
