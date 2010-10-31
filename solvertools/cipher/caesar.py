from solvertools import alphabet
from solvertools.model.language_model import getEnglishModel

def caesar_shift(text, offset, alph=alphabet.ENGLISH):
    """
    Performs a Caesar shift by the given offset.

    If the offset is a letter, it will look it up in the alphabet to convert
    it to a shift. (For example, a shift of 'C' means that 'A' goes to 'C',
    which is the same as a shift of 2.)
        
        >>> print caesar_shift('CAESAR', 13)
        PNRFNE
        >>> print caesar_shift(u'ЦАР', 17, alphabet.ALPHABETS['russian'])
        ЖРБ

    """
    if isinstance(offset, basestring):
        try:
            offset = alph.letter_index(offset) - 1
        except KeyError:
            raise ValueError("The offset should either be an integer, or a "
                             "letter of the alphabet.")

    indices = alph.text_to_indices(text)
    N = len(alph)
    shifted = [(idx - 1 + offset) % N + 1 for idx in indices]
    return alph.indices_to_text(shifted)


def detect_caesar_shift(text, alph=alphabet.ENGLISH):
    """
    Detects the Caesar shift that turns this text into the most reasonable
    English text. Returns the resulting text, the distance shifted
    (from 0 to 25), and the goodness of the result.

        >>> print detect_caesar_shift('TERRA')
        (u'GREEN', 13, -2.4847891081091316)

    """
    theModel = getEnglishModel()
    N = len(alph)
    results = []
    for shift in xrange(N):
        answer = caesar_shift(text, shift)
        results.append((answer, shift, theModel.text_goodness(answer)))
    results.sort(key=lambda x: -x[2])
    return results[0]
    
