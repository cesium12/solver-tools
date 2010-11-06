/*
# Copyright (c) 2010, Alex Schwendner
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
*/

#ifndef __DYNTRIE_DOT_H_INCLUDED__
#define __DYNTRIE_DOT_H_INCLUDED__

#include <vector>
#include <stdint.h>


/**
   A space-inefficient implementation of a dynamic trie. The allowed
   character set is A-Z (uppercase only). Each node stores a 32-bit
   value.
 */
class DynTrie {
  friend class AMTrie;
private:

  class TrieNode {
  public:
    uint32_t data;
    uint32_t next[26];

    TrieNode(void);
  };

  std::vector<TrieNode> slab;

public:

  DynTrie(void); ///< Create a new, empty trie with \c data=0.

  void insert(const char* suffix, uint32_t data_in);

  /**
     Finds the data associated with a given string.

     @requires \c suffix is a pointer to a null-terminated C string
     comprising only uppercase letters.

     @returns The data at the resulting node, or 0 if the node is not
     in the trie.
   */
  uint32_t lookup(const char* suffix) const;

  long nodes(void) const; ///< Returns the number of nodes in the trie.

};


#endif /*__DYNTRIE_DOT_H_INCLUDED__*/
