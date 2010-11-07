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

#include <stdint.h>
#include <stdlib.h>
#include "check.h"
#include "dyntrie.h"


DynTrie::TrieNode::TrieNode(void) :
  data(0) {
  for(int i = 0; i < 26; ++i) {
    next[i] = 0;
  }
}


DynTrie::DynTrie(void) {
  slab.push_back(TrieNode());
}


void DynTrie::insert(const char* suffix, uint32_t data_in) {
  uint32_t p = 0;
  while(*suffix != '\0') {
    CHECK(p < slab.size());
    CHECK('A' <= *suffix && *suffix <= 'Z');
    if(slab[p].next[*suffix - 'A'] == 0) {
      slab[p].next[*suffix - 'A'] = slab.size();
      slab.push_back(TrieNode());
    }
    p = slab[p].next[*suffix - 'A'];
    ++suffix;
  }
  CHECK(p < slab.size());
  slab[p].data = data_in;
}


uint32_t DynTrie::lookup(const char* suffix) const {
  uint32_t p = 0;
  while(*suffix != '\0') {
    CHECK(p < slab.size());
    CHECK('A' <= *suffix && *suffix <= 'Z');
    if(slab[p].next[*suffix - 'A'] == 0) return 0;
    p = slab[p].next[*suffix - 'A'];
    ++suffix;
  }
  CHECK(p < slab.size());
  return(slab[p].data);
}


long DynTrie::nodes(void) const {
  return(slab.size());
}
