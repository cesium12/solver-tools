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

import wrap_thunk
from uncertain import *


class TestMakeUncertainFromList(unittest.TestCase):
    
    def setUp(self):
        self.lst = [( 0,"hello"),
                    (-1,"world")]

    def testEmptyList(self):
        bob = Uncertain([])
        self.assertEqual([v for v in bob], [])
        
    def testWithoutOffset(self):
        bob = Uncertain(self.lst)
        self.assertEqual([v for v in bob], self.lst)
        
    def testIdempotentWithoutOffset(self):
        bob = Uncertain(self.lst)
        self.assertEqual([v for v in bob], self.lst)
        self.assertEqual([v for v in bob], self.lst)
        self.assertEqual([v for v in bob], self.lst)
        self.assertEqual([v for v in bob], self.lst)
        
    def testWithZeroOffset(self):
        bob = Uncertain(self.lst, 0)
        self.assertEqual([v for v in bob], self.lst)
        
    def testWithNegativeOffset(self):
        bob = Uncertain(self.lst, -10)
        self.assertEqual([v for v in bob], map(lambda (w,v): (w-10, v), self.lst))
        
    def testWithPositiveOffset(self):
        bob = Uncertain(self.lst, +10)
        self.assertEqual([v for v in bob], map(lambda (w,v): (w+10, v), self.lst))


class TestMakeUncertainFromGenerator(unittest.TestCase):

    def generator(self):
        yield ( 0,"hello")
        yield (-1,"world")
    
    def setUp(self):
        self.lst = [v for v in self.generator()]
        
    def testWithoutOffset(self):
        bob = Uncertain(self.generator())
        self.assertEqual([v for v in bob], self.lst)
        
    def testWithZeroOffset(self):
        bob = Uncertain(self.generator(), 0)
        self.assertEqual([v for v in bob], self.lst)
        
    def testWithNegativeOffset(self):
        bob = Uncertain(self.generator(), -10)
        self.assertEqual([v for v in bob], map(lambda (w,v): (w-10, v), self.lst))
        
    def testWithPositiveOffset(self):
        bob = Uncertain(self.generator(), +10)
        self.assertEqual([v for v in bob], map(lambda (w,v): (w+10, v), self.lst))


class TestUncertainMerge(unittest.TestCase):

    def testNontrivialMerge(self):
        lst1 = [(0,'a'), (-3,'b'), (-4,'c')]
        lst2 = [(-1, 'd'), (-2, 'e'), (-5, 'f')]
        result = [v for v in Merge([Uncertain(lst1),
                                    Uncertain(lst2)])]
        answer = [(0,'a'), (-1,'d'), (-2,'e'), (-3,'b'), (-4,'c'), (-5,'f')]
        self.assertEqual([v for v in result], answer)

    def testNontrivialMergeIsIdempotent(self):
        lst1 = [(0,'a'), (-3,'b'), (-4,'c')]
        lst2 = [(-1, 'd'), (-2, 'e'), (-5, 'f')]
        result = [v for v in Merge([Uncertain(lst1),
                                    Uncertain(lst2)])]
        answer = [(0,'a'), (-1,'d'), (-2,'e'), (-3,'b'), (-4,'c'), (-5,'f')]
        self.assertEqual([v for v in result], answer)
        self.assertEqual([v for v in result], answer)
        self.assertEqual([v for v in result], answer)
        self.assertEqual([v for v in result], answer)

    def testMergeWithEmpty(self):
        lst1 = [(0,'a'), (-3,'b'), (-4,'c')]
        lst2 = []
        result = [v for v in Merge([Uncertain(lst1),
                                    Uncertain(lst2)])]
        self.assertEqual([v for v in result], lst1)


if __name__ == '__main__':
    unittest.main()
