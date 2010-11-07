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

#include <string.h>
#include "amtrie.h"


const char* AMTrie::MAGIC_STR = "AMTrie1.";

uint32_t AMTrie::AMTrie_helper(const DynTrie &that, uint32_t dpos, uint32_t* trie, uint32_t offset, uint32_t &last_node) {
  uint32_t offset0 = offset;
  uint32_t head = 0;
  uint32_t next[32];
  int p = 0;
  for(int i = 0; i < 26; ++i){
    if(that.slab[dpos].next[i]){
      head |= 1 << i;
      offset += AMTrie_helper(that, that.slab[dpos].next[i], trie, offset, next[p++]);
    }
  }
  uint32_t here = offset;
  trie[offset++] = head;
  trie[offset++] = that.slab[dpos].data;
  for(int i = 0; i < p; ++i){
    trie[offset++] = next[i];
  }
  last_node = here;
  return(offset - offset0);
}

AMTrie::AMTrie() {
  size = 0;
  trie = boost::shared_array<uint32_t>(new uint32_t [size]);
  root = 0;
}

AMTrie::AMTrie(const DynTrie &that) {
  size = 3*that.nodes()-1;
  trie = boost::shared_array<uint32_t>(new uint32_t [size]);
  AMTrie_helper(that, 0, trie.get(), 0, root);
}

uint32_t AMTrie::lookup(const char* s) const {
  uint32_t p = root;
  while(*s != '\0') {
    int index = *s - 'A';
    if(!(trie[p] & (1 << index))) return(0);
    p = trie[p + 2 + __builtin_popcount(trie[p] & (~((~0) << index)))];
    ++s;
  }
  return(trie[p+1]);
}

bool AMTrie::read(FILE* fin) {
  if(feof(fin) || ferror(fin)) return(false);
  char buf[MAGIC_LEN];
  fread(buf, 1, MAGIC_LEN, fin);
  if(feof(fin) || ferror(fin)) return(false);
  if(memcmp(buf, MAGIC_STR, MAGIC_LEN) != 0) return(false);
  fread(&size, sizeof(size), 1, fin);
  fread(&root, sizeof(root), 1, fin);
  if(feof(fin) || ferror(fin)) return(false);
  trie = boost::shared_array<uint32_t>(new uint32_t [size]);
  fread(trie.get(), sizeof(uint32_t), size, fin);
  return(!ferror(fin) && !feof(fin));
}

bool AMTrie::write(FILE* fout) const {
  if(ferror(fout)) return(false);
  fwrite(MAGIC_STR, 1, MAGIC_LEN, fout);
  fwrite(&size, sizeof(size), 1, fout);
  fwrite(&root, sizeof(root), 1, fout);
  fwrite(trie.get(), sizeof(uint32_t), size, fout);
  return(!ferror(fout));
}
