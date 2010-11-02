from bayesinator.core import *
import solvertools.model.language_model as model
import solvertools.wordlist as wordlist


@puzzle_property(str)
def is_word(s):
    return s in wordlist.COMBINED


@entropy_function(str)
def english_model(s):
    return -model.get_english_model().text_logprob(s)
