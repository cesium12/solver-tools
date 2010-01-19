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

def puzzle_logprob(puzzle):
    if isinstance(puzzle, basestring):
        if '?' in puzzle or '#' in puzzle:
            samples = generate_samples(puzzle, 100)
            return max(puzzle_logprob(s) for s in samples)
        elif is_numeric(puzzle):
            return number_logprob(int(puzzle))
        else:
            return english_model.text_logprob(puzzle)
    elif isinstance(puzzle, tuple):
        return sum(puzzle_logprob(part) for part in puzzle)
    else:
        raise ValueError("Puzzles must be made of tuples and strings; got %r"\
                         % puzzle)

def normalize(text):
    return ''.join(t for t in text.upper().replace('-', ' ') if t in
    puzzle_chars)

def entropy(puzzle):
    """
    Like puzzle_logprob, but measured per character. Not currently used.
    """
    n = characters(puzzle)
    return -puzzle_logprob(puzzle)/n

def test():
    print puzzle_logprob('THIS IS A TEST')
    print puzzle_logprob(('THIS', 'IS', 'A', 'TEST'))
    print puzzle_logprob(('16', '2#', '26', '26', '12', '5'))
    print puzzle_logprob(('16', '21', '27', '26', '12', '5'))
    print puzzle_logprob('SNARGLE FROTZ')
    print puzzle_logprob('QZLUX KVJTSEB')
    print puzzle_logprob('BENOISY')
    print puzzle_logprob('BE NOISY')
    print puzzle_logprob('THIS IS A T?ST')
    print puzzle_logprob('THIS ?S A ??ST')

if __name__ == '__main__': test()

