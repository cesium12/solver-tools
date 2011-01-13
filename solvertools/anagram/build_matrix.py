from letter_matrix import letters_to_vec
import numpy as np
from solvertools.puzzlebase.mongo import DB
from solvertools.util import get_datafile

def build_matrix():
    query = DB.alphagrams.find().sort([('alphagram', 1), ('freq', -1)])
    used = set()
    vecs = []
    ranks = []
    for rec in query:
        alpha = rec['alphagram']
        freq = rec['freq']
        if alpha not in used:
            print alpha, freq
            used.add(alpha)
            vecs.append(letters_to_vec(alpha))
            ranks.append(freq)
    matrix = np.vstack(vecs)
    ranks = np.array(ranks)
    
    sort_order = np.lexsort(matrix.T[::-1])
    return matrix[sort_order], ranks[sort_order]

def run():
    matrix, ranks = build_matrix()
    np.save(get_datafile('db/anagram_vectors.npy'), matrix)
    np.save(get_datafile('db/anagram_ranks.npy'), ranks)
    return matrix, ranks

if __name__ == '__main__':
    run()

