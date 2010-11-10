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
#include <assert.h>
#include <string>
#include <string.h>

#include "dict.h"
#include "dyntrie.h"



const char* Dict::MAGIC_STR = "Dict1.";


Dict::Dict() throw () {
  ;
}


Dict::Dict(const char* filename) throw (std::ios_base::failure) {
  bool success = read(filename);
  if(!success) {
    throw new std::ios_base::failure("Input failure while constructing Dict object from file.");
  }
}


Dict::Dict(std::vector<DictEntry> entries) throw () {
  for(size_t i = 0; i < entries.size(); ++i) {
    for(size_t j = 0; j < entries[i].word.length(); ++j) {
      if('a' <= entries[i].word[j] && entries[i].word[j] <= 'z') {
	entries[i].word[j] += 'A' - 'a';
      }
    }
  }
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

  words.push_back(DictEntry());
  DynTrie dyn;
  for(size_t i = 0; i < entries.size(); ++i) {
    dyn.insert(entries[i].word.c_str(), i+1);
    words.push_back(DictEntry(entries[i]));
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
  WordList result;
  result.reserve(fit.size());
  for(size_t i = 0; i < fit.size(); ++i) {
    result.push_back(words[fit[i]]);
  }
  return(result);
}


std::vector<DictEntry> Dict::grep_freq_sorted(std::string regex) const {
  WordFitVec fit = fit_words(Automaton(regex));
  sort(fit.begin(), fit.end(), freq_cmp(this));
  WordList result;
  result.reserve(fit.size());
  for(size_t i = 0; i < fit.size(); ++i) {
    result.push_back(words[fit[i]]);
  }
  return(result);  
}


freq_t Dict::total_freq(std::string regex) const {
  WordFitVec fit = fit_words(Automaton(regex));
  freq_t total = 0;
  for(size_t i = 0; i < fit.size(); ++i) {
    total += words[fit[i]].freq;
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
      if(words[best].freq < words[wordID].freq) {
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

  return(words[best]);
}


bool Dict::read(FILE* fin) {
  if(feof(fin) || ferror(fin)) return(false);
  char buf[MAGIC_LEN];
  fread(buf, 1, MAGIC_LEN, fin);
  if(feof(fin) || ferror(fin)) return(false);
  if(memcmp(buf, MAGIC_STR, MAGIC_LEN) != 0) return(false);
  size_t n;
  fread(&n, sizeof(n), 1, fin);
  if(feof(fin) || ferror(fin)) return(false);
  words.clear();
  words.reserve(n);
  for(size_t i = 0; i < n; ++i) {
    size_t len;
    fread(&len, sizeof(len), 1, fin);
    if(feof(fin) || ferror(fin)) return(false);
    char* buf = new char [len+1];
    fread(buf, sizeof(char), len, fin);
    buf[len] = '\0';
    std::string word(buf);
    delete[] buf;
    if(feof(fin) || ferror(fin)) return(false);
    freq_t freq;
    fread(&freq, sizeof(freq), 1, fin);
    if(feof(fin) || ferror(fin)) return(false);
    words.push_back(DictEntry(word, freq));
  }
  return(trie.read(fin));
}


bool Dict::read(const char* filename) {
  FILE* fin = fopen(filename, "rb");
  if(fin == NULL) return false;
  bool result = read(fin);
  fclose(fin);
  return result;
}


bool Dict::write(FILE* fout) const {
  if(ferror(fout)) return(false);
  fwrite(MAGIC_STR, 1, MAGIC_LEN, fout);
  size_t n = words.size();
  fwrite(&n, sizeof(n), 1, fout);
  for(size_t i = 0; i < n; ++i) {
    size_t len = words[i].word.length();
    fwrite(&len, sizeof(len), 1, fout);
    fwrite(words[i].word.c_str(), sizeof(char), len, fout);
    fwrite(&words[i].freq, sizeof(words[i].freq), 1, fout);
  }

  return(!ferror(fout) && trie.write(fout));
}


bool Dict::write(const char* filename) const {
  FILE* fout = fopen(filename, "wb");
  if(fout == NULL) return false;
  bool result = write(fout);
  fclose(fout);
  return result;
}
