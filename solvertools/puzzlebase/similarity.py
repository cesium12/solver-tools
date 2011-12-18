import logging
import numpy as np
import cPickle as pickle
import codecs
from solvertools.util import get_datafile
from solvertools.wordlist import alphanumeric_only, COMBINED
logger = logging.getLogger(__name__)

class SimilarityMatrix(object):
    """
    A pure-NumPy way of looking up similarities in the singular value
    decomposition of a matrix; this is like what the `divisi2` Python package
    does, but it operates only on a dense matrix and requires no additional C
    code.

    We use this for determining which words are similar to or associated with
    one another.
    """
    def __init__(self, basename='clues'):
        self.U = None
        self.S = None
        self.k = None
        self.labels = None
        self.label_index = {}
        self.basename = basename
    
    def load(self):
        """
        Load the dimensionality-reduced matrix from files in the data/array
        directory, and build an index of terms to row numbers.
        """
        if self.U is None:
            logger.info('Loading similarity matrix')
            self.U = np.load(get_datafile('array/%s.U.npy' % self.basename), 'r+')
            self.S = np.load(get_datafile('array/%s.S.npy' % self.basename), 'r+')
            self.k = len(self.S)
            logger.info('Loading matrix labels')
            self.labels = []
            line_num = 0
            max_lines = self.U.shape[0]

            filename = get_datafile('array/%s.U.labels' % self.basename)

            for line in codecs.open(filename, encoding='utf-8'):
                label = line[:-1]
                self.labels.append(label)
                self.label_index[label] = line_num
                line_num += 1
                if line_num >= max_lines:
                    break

    def similar_to_terms(self, weighted_terms, n=20):
        self.load()
        vec = np.zeros((self.k,))
        found_one = False
        for term, weight in weighted_terms:
            term = alphanumeric_only(term)
            if term in self.label_index:
                row_num = self.label_index[term]
                vec += self.U[row_num] * weight
                found_one = True

        if not found_one:
            return []
        
        # Multiply by sigma to simulate a step of spreading activation in
        # the network.
        assoc_vec = vec * self.S

        # Find the rows with the highest dot product with this vector.
        similarity = np.dot(self.U, assoc_vec)
        most_similar = np.argsort(-similarity)

        results = []
        for index in most_similar[:n]:
            results.append((self.labels[index], similarity[index]))
        return results

    def similar_to_term(self, term, n=20):
        return self.similar_to_terms([(term, 1.)], n)
    
    def pair_similarity(self, term1, term2):
        term1 = alphanumeric_only(term1)
        term2 = alphanumeric_only(term2)
        if term1 not in self.label_index or term2 not in self.label_index:
            return 0
        index1 = self.label_index[term1]
        index2 = self.label_index[term2]
        return np.dot(self.U[index1] * self.S, self.U[index2])
