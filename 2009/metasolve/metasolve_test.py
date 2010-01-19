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
import unittest

import model_freq
import trie
import uncertain
from metasolve import *


class TestMetasolve(unittest.TestCase):

    def setUp(self):
        self.model = model_freq.FreqModel()
        self.model.insert("cows", 4)
        self.model.insert("with", 3)
        self.model.insert("guns", 2)
        self.model.insert("withguns", 1)
        
        self.dict_trie = trie.Trie()
        for word in self.model.all_words():
            self.dict_trie.insert(word)

    def testNoWildsWithUniqueAnswer(self):
        self.assertEqual(
            [(math.log(0.12), ["COWS","WITH"])],
            [x for x in metasolve("COWSWITH", self.dict_trie, self.model)]
            )

    def testNoWildsWithTwoAnswers(self):
        self.assertEqual(
            [(math.log(0.04),  ["COWS","WITHGUNS"]),
             (math.log(0.024), ["COWS","WITH","GUNS"])],
            [x for x in metasolve("COWSWITHGUNS", self.dict_trie, self.model)]
            )

    def testNoWildsWithNoAnswers(self):
        self.assertEqual(
            [],
            [x for x in metasolve("DEADBEEF", self.dict_trie, self.model)]
            )

    def testConstrainedWilds(self):
        self.assertEqual(
            [(math.log(0.04),  ["COWS","WITHGUNS"]),
             (math.log(0.024), ["COWS","WITH","GUNS"])],
            [x for x in metasolve("C??S?ITHG???", self.dict_trie, self.model)]
            )

    def testFreeWild(self):
        self.assertEqual(
            [(math.log(0.12),  ["COWS","WITH"]),
             (math.log(0.09),  ["WITH","WITH"]),
             (math.log(0.06),  ["GUNS","WITH"])],
            [x for x in metasolve("?????ITH", self.dict_trie, self.model)]
            )


if __name__ == '__main__':
    unittest.main()
