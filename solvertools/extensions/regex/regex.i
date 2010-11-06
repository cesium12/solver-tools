%module regex
%include "std_string.i"
%include "std_vector.i"
%include "std_pair.i"

#include <string.h>
#include <vector>

%{
#include "langmodel.h"
#include "regex.h"
%}

typedef LangModel::freq_t freq_t;

namespace std {
  %template(wordlist) vector<pair<string, freq_t> >;
  %template(strlist) vector<string>;
  %template(freqlist) vector<long long>;
}

struct WordFit {
  %immutable;
  const char *word;
  %mutable;
  long long freq;

  WordFit() :
    word(NULL), freq(0) {;}

  WordFit(const char *w, freq_t f) :
    word(w), freq(f) {;}
};

typedef std::vector<WordFit> WordFitVec;

namespace std {
  %template(wordfitvec) vector<WordFit>;
}

WordFitVec regex_match_all(const LangModel &model, const char *regex_in);

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

  LangModel::LangModel(std::vector<std::string> words, std::vector<long long> freqs);

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

int foo(std::vector<std::string> s);

int bar(std::vector<std::string> a, std::vector<long long> b);
