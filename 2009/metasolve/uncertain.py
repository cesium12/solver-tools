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


import heapq


class Uncertain(object):
    """Lazy lists of options sorted by associated log-probabilities.

    The Uncertain class represents an immutable lazy list of options
    with associated log-probabilities, sorted with the most likely
    first.
    """

    def __init__(self, options, offset=0):
        """Construct an instance of Uncertain.

        Args:

          opts: an iterable collection of options. The iter(opts)
            should return the options as pairs of the form (weight,
            value). The weights should all be non-positive to
            represent log-probabilities and they should be sorted in
            decending order.

          offset: an optional argument which may be to adjust the
            weights of all of the options at once. The offset may be
            positive or negative, and the resulting offset weights be
            also be positive or negative. It is the initial input
            weights which must all be non-positive.
        """
        self.__opt_list = []
        self.__opt_iter = iter(options)
        self.__offset = offset

    def Shift(self, dv):
        """Shifts all weights in the set by the same additive offset.

        The offset may be positive or negative, and the resulting
        offset weights may be also be positive or negative.
        """
        bob = Uncertain([])
        bob.__opt_list = self.__opt_list
        bob.__opt_iter = self.__opt_iter
        bob.__offset = self.__offset + dv
        return bob

    def __iter__(self):
        """Returns a fresh iterator over the sorted set of options."""
        return self._UncertainIterator(self.__opt_list,
                                       self.__opt_iter,
                                       self.__offset)

    class _UncertainIterator(object):

        def __init__(self, opt_list, opt_iter, offset=0):
            self.__opt_list = opt_list
            self.__opt_iter = opt_iter
            self.__offset = offset
            self.__index = 0

        def next(self):
            if self.__index < len(self.__opt_list):
                (w,v) = self.__opt_list[self.__index]
                self.__index += 1
                return (w + self.__offset, v)
            else:
                (w,v) = self.__opt_iter.next()
                self.__opt_list.append((w,v))
                self.__index += 1
                return (w + self.__offset, v)


def Merge(option_lists):
    """Merges instances of Uncertain to produce a new instance
    containing all options in the input lists.

    This function can be called with an instance of UncertainIterator,
    but should not be, as then the output instance of Uncertain will
    not be immutable and idempotent.
    """
    
    def MergeIterators():
        heap = []
        for lst in option_lists:
            try:
                it = iter(lst)
                (w,v) = it.next()
                heap.append((-w,v,it))
            except StopIteration:
                pass
        
        heapq.heapify(heap)
        while len(heap) > 0:
            (w,v,it) = heapq.heappop(heap)
            yield (-w,v)
            try:
                (wp,vp) = it.next()
                heapq.heappush(heap,(-wp,vp,it))
            except StopIteration:
                pass

    return Uncertain(MergeIterators())


def MapG(f,generator):
    """Maps a function over the outputs of a generator, returning a
    new generator."""    
    for v in generator:
        yield f(v)
