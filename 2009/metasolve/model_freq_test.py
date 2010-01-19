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


import unittest

from model_freq import *


class TestFreqModel(unittest.TestCase):

    def testEmptyModel(self):
        bob = FreqModel()
        self.assertEqual([], bob.all_words())

    def testSequentialInsert(self):
        bob = FreqModel()

        bob.insert("cows", 5)
        self.assertEqual(["COWS"], bob.all_words())
        self.assertTrue(abs(1-bob.prob("cows")) < 0.001)
        self.assertTrue(abs(1-bob.prob("cows",[])) < 0.001)
        self.assertTrue(abs(1-bob.prob("cows",["cows"])) < 0.001)
        self.assertTrue(abs(1-bob.prob("cows",["moo"])) < 0.001)
        self.assertTrue(abs(bob.prob("with")) < 0.001)
        self.assertTrue(abs(bob.prob("guns")) < 0.001)

        bob.insert("with", 3)
        self.assertTrue(abs(0.625-bob.prob("cows")) < 0.001)
        self.assertTrue(abs(0.375-bob.prob("with")) < 0.001)
        self.assertTrue(abs(bob.prob("guns")) < 0.001)

        bob.insert("guns", 2)
        self.assertTrue(abs(0.5-bob.prob("cows")) < 0.001)
        self.assertTrue(abs(0.3-bob.prob("with")) < 0.001)
        self.assertTrue(abs(0.2-bob.prob("guns")) < 0.001)


if __name__ == '__main__':
    unittest.main()
