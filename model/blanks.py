from language_model import basepath, english_model
from collections import defaultdict
import gzip, os, math
import cPickle as pickle
from string import lowercase

def make_ngram_dict():
    ngrams = {}
    for n in [1, 2, 3]: ngrams[n] = defaultdict(float)
    
    for c1 in lowercase:
        for c2 in lowercase:
            for c3 in lowercase:
                print c1+c2+c3
                prob = english_model.letter_dist[3].prob(c1+c2+c3)
                for d1 in (c1, '.'):
                    for d2 in (c2, '.'):
                        for d3 in (c3, '.'):
                            ngrams[3][d1+d2+d3] += prob
            prob = english_model.letter_dist[2].prob(c1+c2)
            for d1 in (c1, '.'):
                for d2 in (c2, '.'):
                    ngrams[2][d1+d2] += prob
        prob = english_model.letter_dist[1].prob(c1)
        ngrams[1][c1] += prob
        ngrams[1]['.'] += prob

    for n in [1, 2, 3]:
        for key, value in ngrams[n].items():
            ngrams[n][key] = math.log(value, 2)
    return ngrams

picklefn = os.path.join(basepath, 'pickle', 'english.ngramblanks.pickle.gz')
if os.access(picklefn, os.F_OK):
    f = gzip.open(picklefn)
    ngram_blanks = pickle.load(f)
    f.close()
else:
    print "Generating English n-grams with blanks: english.ngramblanks.pickle.gz."
    ngram_blanks = make_ngram_dict()
    out = gzip.open(picklefn, 'w')
    pickle.dump(ngram_blanks, out)
    out.close()

if __name__ == '__main__':
    for key, value in ngram_blanks[3].items():
        print key, value
