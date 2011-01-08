from solvertools.puzzlebase.mongo import *
from solvertools.wordlist import *

# Include words that do not appear in any wordlist but might very well appear
# in a puzzle.
extras = ['XKCD', 'ZYZZLVARIA', 'KONUNDRUM', 'HOCKFIELD', 'IHTFP']

def is_reasonable(word):
    return (word in ENABLE or word in WORDNET or word in Google200K or
            word in NPL or word in CROSSWORD or word in PHONETIC or
            word in IMDB_MOVIES or word in IMDB_ACTORS or word in PHRASES or
            word in MUSICBRAINZ_ARTISTS or word in MUSICBRAINZ_ALBUMS or
            word in MUSICBRAINZ_TRACKS or word in extras)

for rec in DB.words.find().sort([('freq', -1)]):
    text = rec['text']
    freq = rec['freq']
    if is_reasonable(text):
        print "%s,%s" % (text, freq)


# TODO:
    # add musicbrainz
    # rerun 2-word phrases (to fix spacing) followed by google, wordnet,
    # dictionary words
