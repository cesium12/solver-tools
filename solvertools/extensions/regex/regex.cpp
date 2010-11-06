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

#include <iostream>
#include <vector>

#include "automaton.h"
#include "amtrie.h"
#include "langmodel.h"
#include "regex.h"


struct FitWordsState {
  uint_fast32_t graphNode; //< The state of the automaton.
  uint32_t trieNode;       //< The position in the dictionary trie.

  inline FitWordsState() {}
  inline FitWordsState(uint_fast32_t gn, uint32_t tn) :
    graphNode(gn), trieNode(tn) {;}
};


WordFitVec fitWords(const LangModel &model, const Automaton &automaton) {

  const AMTrie &dict = model.getDict();

  WordFitVec fit;

  std::vector<FitWordsState> stack;
  stack.push_back(FitWordsState(automaton.getStartState(), dict.getRoot()));

  while(!stack.empty()) {
    FitWordsState pos = stack.back();
    stack.pop_back();
    const Automaton::Node &s = automaton.getNode(pos.graphNode);
    uint32_t graphEdges = s.getFingerprint();
    uint32_t trieEdges  = dict.getPos(pos.trieNode);
    uint32_t wordID     = dict.getPos(pos.trieNode+1);
    uint32_t edges      = graphEdges & trieEdges;

    if(wordID && pos.graphNode == automaton.getAcceptState()) {
      // it's a word!
      fit.push_back(WordFit(model.id_to_word(wordID).c_str(), model.id_to_freq(wordID)));
    }

    // handle letter edges
    uint32_t head = pos.trieNode + 2;
    while(edges) {
      uint_fast32_t index = __builtin_ctz(edges);
      uint32_t dictPos2 = head + __builtin_popcount(trieEdges & (~((~0) << index)));
      stack.push_back(FitWordsState(s.getLetterDest(index),
				    dict.getPos(dictPos2)));
      edges &= ~(1 << index);
    }

    // handle epsilon edges
    for(uint_fast32_t i = 0; i < s.getNumEpsilonEdges(); ++i) {
      stack.push_back(FitWordsState(s.getEpsilonDest(i),
				    pos.trieNode));
    }
  }

  return(fit);  
}


WordFitVec regex_match_all(const LangModel &model, const char *regex) {
  Automaton prob(regex);
  WordFitVec result = fitWords(model, prob);
  sort(result.begin(), result.end());
  return result;
}
