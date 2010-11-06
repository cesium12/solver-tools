%module regex
#include <string.h>
#include <vector>

#include "langmodel.h"


typedef LangModel::freq_t freq_t;

struct WordFit {
  %feature("immutable");
  const char *word;
  freq_t freq;
  
  WordFit(const char *w, freq_t f) :
    word(w), freq(f) {;}
};

typedef std::vector<WordFit> WordFitVec;

WordFitVec regex_match_all(const LangModel &model, const char *regex_in);

