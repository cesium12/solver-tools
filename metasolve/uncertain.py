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

    Representation invariants:
    * Attribute __make_iter should be an idempotent thunk which
      returns an iterator over the list of options. This thunk should
      be idempotent (i.e. multiple calls should return independant
      iterators over the same collection) so that the instance of
      Uncertain can be immutable. The list of options should be
      structured as a list of pairs of the form (weight, value). The
      weights should all be non-positive to represent
      log-probabilities and they should be sorted in decending order.
    * Attribute __offset should be a real number.

    Abstraction function:
      The lazy list of options is the list iterated over by the result
      of calling __make_iter, with weights additively offset by
      __offset.
    """

    def __init__(self, make_iter, offset=0):
        """Construct an instance of Uncertain.

        Args:

          make_iter: an idempotent thunk which returns an iterator
            over the list of options. This thunk should be idempotent
            (i.e. multiple calls should return independant iterators
            over the same collection) so that the instance of
            Uncertain can be immutable. The list of options should be
            structured as a list of pairs of the form (weight,
            value). The weights should all be non-positive to
            represent log-probabilities and they should be sorted in
            decending order.

          offset: an optional argument which may be to adjust the
            weights of all of the options at once. The offset may be
            positive or negative, and the resulting offset weights be
            also be positive or negative. It is the initial input
            weights which must all be non-positive.
        """
        self.__make_iter = make_iter
        self.__offset = offset

    def AdmisiveHeuristic(self):
        """An upper bound on the weights of the options."""
        return self.__offset

    def Shift(self, dv):
        """Shifts all weights in the set by the same additive offset.

        The offset may be positive or negative, and the resulting
        offset weights be also be positive or negative.
        """
        return Uncertain(self.__make_iter, self.__offset + dv)

    def __iter__(self):
        """Returns a fresh iterator over the sorted set of options."""
        return UncertainIterator(iter(self.__make_iter()),
                                 self.__offset)


class UncertainIterator(Uncertain):
    """An iterator over a lazy list of options with associated
    log-probabilities, sorted with the most likely first.

    This will usually be the result of calling iter on some instance
    of Uncertain.

    Representation invariants:
    * Attribute __opt_iter should be an iterator over a set of options
      structured as pairs of the form (weight, value). The weights
      should all be non-positive to represent log-probabilities and
      they should be sorted in decending order.
    * Attribute __offset should be a real number.
    * Attribute __offset should be a real number which is greater than
      or equal to all of the weights in the unoffset option set
      iterated over by __opt_iter.
    """

    def __init__(self, opt_iter, offset=0):
        """Construct an instance of UncertainIterator.

        The argument opt_iter should be an iterator over a set of
        options structured as pairs of the form (weight, value). The
        weights should all be non-positive to represent
        log-probabilities and they should be sorted in decending
        order.

        The optional argument offset may be given to adjust the
        weights of all of the options at once. The offset may be
        positive or negative, and the resulting offset weights be also
        be positive or negative. It is the initial input weights which
        must all be non-positive.
        """
        
        self.__opt_iter = opt_iter
        self.__offset = offset
        self.__hval = 0

    def AdmisiveHeuristic(self):
        """Returns a real number which should be greater than or equal
        to the weights of any options in the option set.
        """
        
        return self.__hval + self.__offset

    def next(self):
        """Returns the next most likely option in the option set as a
        pair (weight, value).

        Raises UncertainSortedViolation if it discovers that the
        options are not sorted as specified by the representation
        invariant.
        """
        
        (w,v) = self.__opt_iter.next()
        if w > self.__hval:
            raise UncertainSortedViolation()
        self.__hval = w
        return (w + self.__offset, v)


class UncertainSortedViolation:
    pass


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
            w = lst.AdmisiveHeuristic()
            it = iter(lst)
            heap.append((-w,True,0,it))

        heapq.heapify(heap)
        while len(heap) > 0:
            (w,fake,v,it) = heapq.heappop(heap)
            try:
                (wp,vp) = it.next()
                heapq.heappush(heap,(-wp,False,vp,it))
            except StopIteration:
                pass
            if not fake:
                yield (-w,v)

    return Uncertain(MergeIterators)


def MapG(f,generator):
    """Maps a function over the outputs of a generator, returning a
    new generator."""    
    for v in generator:
        yield f(v)
