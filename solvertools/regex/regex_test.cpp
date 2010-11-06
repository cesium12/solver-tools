#include <iostream>
#include <stdint.h>
#include <string>
#include <vector>

#include "regex.h"


int main() {

  std::vector<std::pair<std::string, uint64_t> > words;
  words.push_back(make_pair(std::string("FELIX"),  363));
  words.push_back(make_pair(std::string("HBOMB"),   12));
  words.push_back(make_pair(std::string("HECTOR"), 900));
  words.push_back(make_pair(std::string("HELIX"),    1));
  words.push_back(make_pair(std::string("HELL"),    19));
  words.push_back(make_pair(std::string("HELLO"),   24));
  words.push_back(make_pair(std::string("HELP"),    16));
  words.push_back(make_pair(std::string("WORLD"),  111));

  LangModel model(words);

  WordFitVec matches = regex_match_all(model, "(f|h)el(i|t|l).*");
  for(int i = 0; i < matches.size(); ++i) {
    std::cout << matches[i].word << '\t' << matches[i].freq << std::endl;
  }

  return(0);
}
