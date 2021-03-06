from solvertools.puzzlebase.mongo import DB

def get_anagrams(alphagram):
    for entry in DB.wordplay.find({'alphagram': alphagram}):
        yield entry['text'], entry['freq']

