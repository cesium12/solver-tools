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


class Trie:
    """A Trie storing values."""

    def __init__(self):
        """Creates a new, empty trie."""
        self.value = None
        self.next_dict = {}

    def insert(self, it, val=True):
        """Given an iterable object, inserts it into the trie.

        Argument it is the iterable object.
        Argument val is the value to insert. If unspecified, True will
          be inserted.
        """
        it = iter(it)
        here = self

        while True:
            try:
                x = it.next()
                if not here.next_dict.has_key(x):
                    here.next_dict[x] = Trie()
                here = here.next_dict[x]
            except StopIteration:
                here.value = val
                break
        
    def lookup(self, it, default=None):
        """Given an iterable object, look it up in the trie and return
        the associated data.

        Argument it is the iterable object.
        Argument default is the value to return if the object is not
          found in the trie. If unspecified, None will be returned.
        """
        it = iter(it)
        here = self

        while True:
            try:
                x = it.next()
                if here.next_dict.has_key(x):
                    here = here.next_dict[x]
                else:
                    return default
            except StopIteration:
                return here.value
        
