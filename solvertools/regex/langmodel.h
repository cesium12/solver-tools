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

#ifndef __LANGMODEL_DOT_H_INCLUDED__
#define __LANGMODEL_DOT_H_INCLUDED__

#include <stdint.h>
#include <string>
#include <vector>
#include "amtrie.h"

class LangModel {
public:

  typedef uint64_t freq_t;
  typedef std::string string;
  typedef std::vector<string> WordList;
  typedef std::vector<freq_t> FreqList;

private:

  AMTrie dict; ///< A dictionary containing the known words. The data
	       ///associated with each word is the word's unique
	       ///identifier >= 1.
  WordList word_list; ///< A vector mapping unique identifiers to
		      ///words.
  FreqList freq_list; ///< A vector mapping unique identifiers to word
		      ///frequencies.
  

public:

  LangModel(const std::vector<std::pair<std::string, freq_t> > &words);

  /**
     Returns the dictionary.
   */
  inline const AMTrie &getDict() const;

  /**
     Returns the unique ID number associated with a word, or zero if
     the word is not in the dictionary.
   */
  inline uint32_t word_to_id(const char* s) const;

  /**
     Returns the string represented by a given ID number. If the ID
     number is invalid, returns the empty string.
   */
  inline std::string id_to_word(unsigned long i) const;

  inline freq_t id_to_freq(unsigned long i) const;

};


inline const AMTrie &LangModel::getDict() const {
  return(dict);
}

inline uint32_t LangModel::word_to_id(const char* s) const {
  return(dict.lookup(s));
}

inline std::string LangModel::id_to_word(unsigned long i) const {
  if(i < 0 || i >= word_list.size())
    return std::string("");
  return(word_list[i]);
}

inline LangModel::freq_t LangModel::id_to_freq(unsigned long i) const {
  if(i < 0 || i >= freq_list.size())
    return 0;
  return(freq_list[i]);
}

#endif /*__LANGMODEL_DOT_H_INCLUDED__*/
