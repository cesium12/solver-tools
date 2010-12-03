from nltk.corpus import wordnet
from solvertools.util import get_dictfile
def run():
    out = open(get_dictfile('wordnet.txt'), 'w')
    biglist = list(name.replace('_', ' ') for name in wordnet.all_lemma_names())
    biglist.sort()
    for item in biglist:
        print >> out, item
        print item

if __name__ == '__main__':
    run()
