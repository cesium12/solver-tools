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

#ifndef __AMTRIE_DOT_H_INCLUDED__
#define __AMTRIE_DOT_H_INCLUDED__

#include <boost/shared_array.hpp>
#include <cstdio>
#include <stdint.h>
#include <stdlib.h>
#include "dyntrie.h"


/** A space-efficient implementation of a trie. The character set is
    the capital letters.
 */
class AMTrie {
private:
  /** The array containing the data for the trie. The array of \c
      uint32_t words contains the nodes of the trie in a very special
      format. Each node has a variable size, depending on the number
      of exiting edges. If a node has \a k outgoing edges, then the
      node comprises \a k+2 words. These words have the following
      format:

      - word 0: a 32-bit fingerprint specifying which outgoing edges are
        present. For each of A-Z, the corresponding bit 0-25 is set if
        that edge is present. Bits 26-31 are unused.
      - word 1: 32-bit data
      - words 2-?: for each outgoing edge present, a 32-bit integer
        specifying the index in the array of the target node of the
        edge. The edges are listed in alphabetical order.
   */
  boost::shared_array<uint32_t> trie;
  size_t size; ///< The length of the \c trie array.
  uint32_t root; ///< The index in the \c trie array of the first word
		 ///of the root node.

protected:
  static const char* MAGIC_STR; ///< The "magic string" to written to
				///a file at the start of an AMTrie.
  static const size_t MAGIC_LEN = 8; ///< The length of the "magic
				     ///string".

public:

  /// Returns the index of the root node.
  inline uint32_t getRoot() const {
    return root;
  }
  /// Returns the word at a specified 32-bit index.
  inline uint32_t getPos(uint32_t i) const {
    return trie[i];
  }
  /// Returns the number of valid indices.
  inline size_t getSize() const {
    return size;
  }

  AMTrie();
  AMTrie(const DynTrie &that);

  /**
     Finds the data associated with a given string.

     @requires \c suffix is a pointer to a null-terminated C string
     comprising only uppercase letters.

     @returns The data at the resulting node, or 0 if the node is not
     in the trie.
   */
  uint32_t lookup(const char* s) const;


  /**
     Reads an AMTrie from a file.
     @returns \c true if the AMTrie was successfully read.
  */
  bool read(FILE* fin);

  /**
     Writes an AMTrie to a file.
     @returns \c true if the AMTrie was successfully written.
  */
  bool write(FILE* fout) const;

private:

  static uint32_t AMTrie_helper(const DynTrie &that, uint32_t dpos, uint32_t* trie, uint32_t offset, uint32_t &last_node);
};


#endif /*__AMTRIE_DOT_H_INCLUDED__*/
