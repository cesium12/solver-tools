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

#include <gtest/gtest.h>
#include <stdlib.h>
#include "dyntrie.h"


TEST(DynTrieTest, InsertLookupMany) {
  DynTrie trie;
  unsigned int state = 0;
  for(int i = 0; i < 1000; ++i) {
    char buffer[20];
    int len = (rand_r(&state) % 10) + 1;
    for(int j = 0; j < len; ++j) {
      buffer[j] = 'A' + (rand_r(&state) % 26);
    }
    buffer[len] = '\0';

    uint32_t data = rand_r(&state);
    trie.insert(buffer, data);
    EXPECT_EQ(data, trie.lookup(buffer));
  }
}

TEST(DynTrieTest, SimpleLookup) {
  DynTrie trie;

  trie.insert("FOO", 5);
  trie.insert("FOOD", 6);
  trie.insert("BAR", 7);
  trie.insert("BAZ", 8);
  trie.insert("QUAX", 9);
  trie.insert("QUAAX", 10);
  trie.insert("QUAXQUAX", 11);

  EXPECT_EQ(5, trie.lookup("FOO"));
  EXPECT_EQ(6, trie.lookup("FOOD"));
  EXPECT_EQ(7, trie.lookup("BAR"));
  EXPECT_EQ(8, trie.lookup("BAZ"));
  EXPECT_EQ(9, trie.lookup("QUAX"));
  EXPECT_EQ(10, trie.lookup("QUAAX"));
  EXPECT_EQ(11, trie.lookup("QUAXQUAX"));

  EXPECT_EQ(0, trie.lookup("COWS"));
  EXPECT_EQ(0, trie.lookup("WITH"));
  EXPECT_EQ(0, trie.lookup("GUNS"));
}
