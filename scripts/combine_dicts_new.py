from solvertools.puzzlebase.mongo import *
from solvertools.wordlist import *
from solvertools.util import get_dictfile

# Include words that do not appear in any wordlist but might very well appear
# in a puzzle.
extras = ['XKCD', 'ZYZZLVARIA', 'KONUNDRUM', 'HOCKFIELD', 'IHTFP']

def is_google_worthy(word):
    if word.startswith('WWW') or word.endswith('COM'):
        return False
    return word in Google200K and Google200K[word] >= 100000

def is_reasonable(word):
    return (word in ENABLE or word in WORDNET or
            word in NPL or word in CROSSWORD or word in PHONETIC or
            word in IMDB_MOVIES or word in IMDB_ACTORS or word in PHRASES or
            word in MUSICBRAINZ_ARTISTS or word in MUSICBRAINZ_ALBUMS or
            word in MUSICBRAINZ_TRACKS or word in extras or word in WIKTIONARY
            or is_google_worthy(word))

out = open(get_dictfile('sages_combined_new'), 'w')
for rec in DB.words.find().sort([('freq', -1)]):
    text = rec['text']
    freq = rec['freq']
    if is_reasonable(text):
        print "%s,%s" % (asciify(text), freq)
        print >> out, "%s,%s" % (asciify(text), freq)
out.close()

