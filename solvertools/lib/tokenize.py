"""
Rob Speer's implementation of the vague NLP consensus for how text should
be tokenized. Borrowed from ConceptNet 4.0rc2.
"""

import string
import re
    
def tokenize(text):
    r"""
    Tokenizing a sentence inserts spaces in such a way that it separates
    punctuation from words, splits up contractions, and generally does what
    a lot of natural language tools (especially parsers) expect their
    input to do.

        >>> en_nl.tokenize("Time is an illusion. Lunchtime, doubly so.")
        'Time is an illusion . Lunchtime , doubly so .'
        >>> untok = '''
        ... "Very deep," said Arthur, "you should send that in to the
        ... Reader's Digest. They've got a page for people like you."
        ... '''
        >>> tok = en_nl.tokenize(untok)
        >>> tok
        "`` Very deep , '' said Arthur , `` you should send that in to the Reader 's Digest . They 've got a page for people like you . ''"
        >>> en_nl.untokenize(tok)
        '"Very deep," said Arthur, "you should send that in to the Reader\'s Digest. They\'ve got a page for people like you."'
        >>> en_nl.untokenize(tok) == untok.replace('\n', ' ').strip()
        True

    """
    step0 = text.replace('\r', '').replace('\n', ' ')
    step1 = step0.replace(" '", " ` ").replace("'", " '").replace("n 't", 
    " n't").replace("cannot", "can not")
    step2 = re.sub('"([^"]*)"', r" `` \1 '' ", step1)
    step3 = re.sub(r'([.,:;?!%]+) ', r" \1 ", step2)
    step4 = re.sub(r'([.,:;?!%]+)$', r" \1", step3)
    step5 = re.sub(r'([()\[\]{}<>|])', r" \1 ", step4)
    return re.sub(r'  +', ' ', step5).strip()

def untokenize(text):
    """
    Untokenizing a text undoes the tokenizing operation, restoring
    punctuation and spaces to the places that people expect them to be.

    Ideally, `untokenize(tokenize(text))` should be identical to `text`,
    except for line breaks.
    """
    step1 = text.replace("`` ", '"').replace(" ''", '"')
    step2 = step1.replace(" ( ", " (").replace(" ) ", ") ")
    step3 = re.sub(r' ([.,:;?!%]+)([ \'"`])', r"\1\2", step2)
    step4 = re.sub(r' ([.,:;?!%]+)$', r"\1", step3)
    step5 = step4.replace(" '", "'").replace(" n't", "n't").replace(
      "can not", "cannot")
    step6 = step5.replace(" ` ", " '")
    return step6.strip()

def tokenize_list(text):
    return tokenize(text).split()

def untokenize_list(text):
    return untokenize(' '.join(text))
