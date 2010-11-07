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

#include <algorithm>
#include <string>

#include "dict.h"
#include "dyntrie.h"


Dict::Dict(std::vector<DictEntry> entries) {
  sort(entries.begin(), entries.end());
  size_t p = 0;
  for(size_t i = 1; i < entries.size(); ++i) {
    if(entries[i].freq <= 0) continue;
    if(entries[i].word == entries[p].word) {
      entries[p].freq += entries[i].freq;
    } else {
      ++p;
      entries[p] = entries[i];
    }
  }
  if(entries.size() > 0) {
    entries.resize(p+1);
  }

  word_list.push_back(std::string(""));
  freq_list.push_back(0);
  DynTrie dyn;
  for(size_t i = 0; i < entries.size(); ++i) {
    dyn.insert(entries[i].word.c_str(), i+1);
    word_list.push_back(entries[i].word);
    freq_list.push_back(entries[i].freq);
  }
  trie = AMTrie(dyn);
}


Dict::WordFitVec Dict::fit_words(const Automaton &automaton) const {

  WordFitVec fit;

  std::vector<FitWordsState> stack;
  stack.push_back(FitWordsState(automaton.getStartState(), trie.getRoot()));

  while(!stack.empty()) {
    FitWordsState pos = stack.back();
    stack.pop_back();
    const Automaton::Node &s = automaton.getNode(pos.graphNode);
    uint32_t graphEdges = s.getFingerprint();
    uint32_t trieEdges  = trie.getPos(pos.trieNode);
    uint32_t wordID     = trie.getPos(pos.trieNode+1);
    uint32_t edges      = graphEdges & trieEdges;

    if(wordID && pos.graphNode == automaton.getAcceptState()) {
      // it's a word!
      fit.push_back(wordID);
    }

    // handle letter edges
    uint32_t head = pos.trieNode + 2;
    while(edges) {
      uint_fast32_t index = __builtin_ctz(edges);
      uint32_t dictPos2 = head + __builtin_popcount(trieEdges & (~((~0) << index)));
      stack.push_back(FitWordsState(s.getLetterDest(index),
				    trie.getPos(dictPos2)));
      edges &= ~(1 << index);
    }

    // handle epsilon edges
    for(uint_fast32_t i = 0; i < s.getNumEpsilonEdges(); ++i) {
      stack.push_back(FitWordsState(s.getEpsilonDest(i),
				    pos.trieNode));
    }
  }

  if (fit.size() == 0) {
    return fit;
  }
  sort(fit.begin(), fit.end());
  size_t n = fit.size();
  size_t k = 1;
  for (size_t i = 1; i < n; ++i) {
    if (fit[i] != fit[i-1]) {
      fit[k] = fit[i];
      ++k;
    }
  }
  fit.resize(k);

  return(fit);  
}


std::vector<DictEntry> Dict::grep(std::string regex) const {
  WordFitVec fit = fit_words(Automaton(regex));
  std::vector<DictEntry> result;
  result.reserve(fit.size());
  for(size_t i = 0; i < fit.size(); ++i) {
    result.push_back(DictEntry(word_list[fit[i]], freq_list[fit[i]]));
  }
  return(result);
}


std::vector<DictEntry> Dict::grep_freq_sorted(std::string regex) const {
  WordFitVec fit = fit_words(Automaton(regex));
  sort(fit.begin(), fit.end(), freq_cmp(this));
  std::vector<DictEntry> result;
  result.reserve(fit.size());
  for(size_t i = 0; i < fit.size(); ++i) {
    result.push_back(DictEntry(word_list[fit[i]], freq_list[fit[i]]));
  }
  return(result);  
}


freq_t Dict::total_freq(std::string regex) const {
  WordFitVec fit = fit_words(Automaton(regex));
  freq_t total = 0;
  for(size_t i = 0; i < fit.size(); ++i) {
    total += freq_list[i];
  }
  return(total);
}


DictEntry Dict::best_match(std::string regex) const {

  Automaton automaton(regex);
  uint32_t best = 0;

  std::vector<FitWordsState> stack;
  stack.push_back(FitWordsState(automaton.getStartState(), trie.getRoot()));

  while(!stack.empty()) {
    FitWordsState pos = stack.back();
    stack.pop_back();
    const Automaton::Node &s = automaton.getNode(pos.graphNode);
    uint32_t graphEdges = s.getFingerprint();
    uint32_t trieEdges  = trie.getPos(pos.trieNode);
    uint32_t wordID     = trie.getPos(pos.trieNode+1);
    uint32_t edges      = graphEdges & trieEdges;

    if(wordID && pos.graphNode == automaton.getAcceptState()) {
      if(freq_list[best] < freq_list[wordID]) {
	best = wordID;
      }
    }

    // handle letter edges
    uint32_t head = pos.trieNode + 2;
    while(edges) {
      uint_fast32_t index = __builtin_ctz(edges);
      uint32_t dictPos2 = head + __builtin_popcount(trieEdges & (~((~0) << index)));
      stack.push_back(FitWordsState(s.getLetterDest(index),
				    trie.getPos(dictPos2)));
      edges &= ~(1 << index);
    }

    // handle epsilon edges
    for(uint_fast32_t i = 0; i < s.getNumEpsilonEdges(); ++i) {
      stack.push_back(FitWordsState(s.getEpsilonDest(i),
				    pos.trieNode));
    }
  }

  return(DictEntry(word_list[best], freq_list[best]));
}
