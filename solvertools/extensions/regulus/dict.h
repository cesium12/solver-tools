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

#ifndef __DICT_DOT_H_INCLUDED__
#define __DICT_DOT_H_INCLUDED__

#include <iostream>
#include <stdint.h>
#include <string>
#include <vector>
#include "amtrie.h"
#include "automaton.h"


typedef uint64_t freq_t;


struct DictEntry {
  std::string word;
  freq_t freq;

  DictEntry() :
    word(""), freq(0) {;}

  DictEntry(const char *w, freq_t f) :
    word(std::string(w)), freq(f) {;}

  DictEntry(const std::string &w, freq_t f) :
    word(w), freq(f) {;}
};

inline bool operator <(const DictEntry &a, const DictEntry &b) {
  return a.word < b.word;
}


class Dict {
public:

  typedef std::string string;
  typedef std::vector<DictEntry> WordList;


protected:
  static const char* MAGIC_STR; ///< The "magic string" to written to
				///a file at the start of an AMTrie.
  static const size_t MAGIC_LEN = 6; ///< The length of the "magic
                                     ///string".


private:

  AMTrie trie; ///< A dictionary containing the known words. The data
	       ///associated with each word is the word's unique
	       ///identifier >= 1.
  WordList words; ///< A vector mapping unique identifiers to words
                  ///and their associated frequencies.


public:

  /**
     Constructs a new (empty) dictionary.
   */
  Dict() throw ();

  /**
     Constructs a new dictionary object based on a binary file.
   */
  explicit Dict(const char* filename) throw (std::ios_base::failure);

  /**
     Constructs a new dictionary from the given word->frequency map.
     Assumes that each word is given at most once.
   */
  Dict(std::vector<DictEntry> entries) throw ();

  /**
     Returns a list of all words matching the given regular
     expression, sorted alphabetically.
   */
  std::vector<DictEntry> grep(std::string regex) const;

  /**
     Returns a list of all words matching the given regular
     expression, sorted by word frequency.
   */
  std::vector<DictEntry> grep_freq_sorted(std::string regex) const;

  /**
     Returns the sum of the frequencies of all words matching the
     given regular expression.
   */
  freq_t total_freq(std::string regex) const;

  /**
     Among the words matching the given regular expression, returns
     the word with the heightest frequency.  Among matching words with
     equal frequencies, returns the word which comes first
     alphabetically.  If no words in the dictionary match the regular
     expression, returns DictEntry("", 0).
   */
  DictEntry best_match(std::string regex) const;

  /**
     Reads a binary representation of a dictionary from a file.
     @returns \c true if the Dict was successfully read.
  */
  bool read(FILE* fin);
  bool read(const char* filename);

  /**
     Writes a binary representation of a dictionary to a file.
     @returns \c true if the Dict was successfully written.
  */
  bool write(FILE* fout) const;
  bool write(const char* filename) const;


private:

  struct FitWordsState {
    uint_fast32_t graphNode; //< The state of the automaton.
    uint32_t trieNode;       //< The position in the dictionary trie.

    inline FitWordsState() {}
    inline FitWordsState(uint_fast32_t gn, uint32_t tn) :
      graphNode(gn), trieNode(tn) {;}
  };

  typedef uint32_t WordFit;
  typedef std::vector<WordFit> WordFitVec;

  struct freq_cmp {
    const Dict *dict;
    freq_cmp(const Dict *dict_ptr) :
      dict(dict_ptr) {;}
    inline bool operator ()(const WordFit &a, const WordFit &b) {
      freq_t f1 = dict->words[a].freq;
      freq_t f2 = dict->words[b].freq;
      if (f1 != f2) {
	return f1 > f2;
      } else {
	return a < b;
      }
    }
  };

  Dict::WordFitVec fit_words(const Automaton &automaton) const;

};


#endif /*__DICT_DOT_H_INCLUDED__*/
