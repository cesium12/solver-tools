%module regulus
%include "exception.i"
%include "std_string.i"
%include "std_vector.i"
%include "std_pair.i"
%include "stdint.i"

#include <iostream>
#include <stdint.h>
#include <string>
#include <vector>

%{
#include <stdint.h>
typedef uint64_t freq_t;
#include "amtrie.h"
#include "automaton.h"
#include "dict.h"
%}
typedef uint64_t freq_t;


namespace std {
  %template(dictvector) vector<DictEntry>;
};


%exception {
    try {
        $action
    } catch(Automaton::SpecException &e) {
        PyErr_SetString(PyExc_ValueError,e.what());
        return NULL;
    }
}

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

class Dict {
public:

  Dict() throw ();
  Dict(std::vector<DictEntry> entries);

  bool read(const char* filename);
  bool write(const char* filename) const;

  std::vector<DictEntry> grep(std::string regex) const;
  std::vector<DictEntry> grep_freq_sorted(std::string regex) const;
  freq_t total_freq(std::string regex) const;
  DictEntry best_match(std::string regex) const;

};
