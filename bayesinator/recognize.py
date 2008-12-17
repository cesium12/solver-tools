from model.language_model import english_model, LanguageModel,\
  unigram_sampler, is_numeric
from model.numbers import number_logprob
import random
import string

puzzle_chars = string.uppercase + string.digits + "'?# "

def characters(puzzle):
    if isinstance(puzzle, basestring):
        return len(puzzle)
    else:
        return sum(characters(part) for part in puzzle)

def character_sample(char):
    if char == '?': return unigram_sampler(english_model)
    elif char == '#': return random.choice(string.digits)
    else: return char

def generate_samples(text, n):
    for i in xrange(n):
        yield ''.join(character_sample(c) for c in text)

def recursive_likelihood(puzzle):
    if isinstance(puzzle, basestring):
        if '?' in puzzle or '#' in puzzle:
            samples = generate_samples(puzzle, 100)
            return sum(recursive_likelihood(s) for s in samples)/100
        elif is_numeric(puzzle):
            return number_logprob(int(puzzle))
        else:
            return english_model.text_logprob(puzzle)
    elif isinstance(puzzle, list):
        return sum(recursive_likelihood(part) for part in puzzle)
    else:
        raise ValueError("Puzzles must be made of lists and strings; got %r"\
                         % puzzle)

def normalize(text):
    return ''.join(t for t in text.upper().replace('-', ' ') if t in
    puzzle_chars)

def entropy(puzzle):
    """
    Output the negative log likelihood that this puzzle is, or is close to, the
    'un-puzzle' (a data structure that does not need to be deciphered).
    """
    n = characters(puzzle)
    return -recursive_likelihood(puzzle)/n

def test():
    print entropy('THIS IS A TEST')
    print entropy(['THIS', 'IS', 'A', 'TEST'])
    print entropy(['16', '21', '26', '26', '12', '5'])
    print entropy(['16', '21', '27', '26', '12', '5'])
    print entropy('SNARGLE FROTZ')
    print entropy('BENOISY')
    print entropy('BE NOISY')
test()
