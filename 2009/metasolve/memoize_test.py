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

from memoize import *


class MemoizeUnitTest(unittest.TestCase):

    def setUp(self):
        def fibRec(n, modulus=None):
            if n == 0:
                ans = 0
            elif n <= 2:
                self.counter += 1
                ans = 1
            else:
                ans = fibRec(n-1) + fibRec(n-2)
            if modulus:
                ans = ans % modulus
            return ans

        @Memoize
        def fibMemo(n, modulus=None):
            if n == 0:
                ans = 0
            elif n <= 2:
                self.counter += 1
                ans = 1
            else:
                ans = fibMemo(n-1) + fibMemo(n-2)
            if modulus:
                ans = ans % modulus
            return ans

        self.fibRec  = fibRec
        self.fibMemo = fibMemo
        self.counter = 0

    def testIsFib(self):
        self.assertEqual([self.fibRec(x) for x in range(0,9)],
                         [0,1,1,2,3,5,8,13,21])
        self.assertEqual([self.fibMemo(x) for x in range(0,9)],
                         [0,1,1,2,3,5,8,13,21])
        self.assertEqual([self.fibRec(x,None) for x in range(0,9)],
                         [0,1,1,2,3,5,8,13,21])
        self.assertEqual([self.fibMemo(x,None) for x in range(0,9)],
                         [0,1,1,2,3,5,8,13,21])
        self.assertEqual([self.fibRec(x,4) for x in range(0,9)],
                         [0,1,1,2,3,1,0,1,1])
        self.assertEqual([self.fibMemo(x,4) for x in range(0,9)],
                         [0,1,1,2,3,1,0,1,1])
        self.assertEqual([self.fibRec(x,10) for x in range(0,9)],
                         [0,1,1,2,3,5,8,3,1])
        self.assertEqual([self.fibMemo(x,10) for x in range(0,9)],
                         [0,1,1,2,3,5,8,3,1])

    def testNoMemoizeFib(self):
        for k in range(1,15):
            self.counter = 0
            v = self.fibRec(k)
            self.assertEqual(v, self.counter)

    def testYesMemoizeFib(self):
        for k in range(3,15):
            self.counter = 0
            self.fibMemo(k)
            self.assertTrue(self.counter <= 2)


if __name__ == '__main__':
    unittest.main()
