import bayesinator.alphabet as alphabet
from bayesinator.core import *
import solvertools.model.language_model as model
import solvertools.wordlist as wordlist



@puzzle_property(basestring)
def word(s):
    return s in wordlist.COMBINED


@entropy_function(alphabet.english)
def english_model(s):
    return -model.get_english_model().text_logprob(s)
