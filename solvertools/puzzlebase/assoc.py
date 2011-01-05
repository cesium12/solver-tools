from solvertools.wordlist import alphanumeric_only
from solvertools.puzzlebase.mongo import DB
from math import log
MIN = -1000000.0

def relation_goodness(rel, word1, word2):
    query = DB.relations.find_one(
      {'rel': rel,
       'words': [word1, word2]}
    )
    if not query:
        return MIN
    log_numer = log(query['freq'])
    log_denom = 0.0
    for word in (word1, word2):
        key = rel+' '+word
        query = db.totals.find_one({'_id': key})
        if not query:
            return MIN
        log_denom += log(query['total'])
    return log_numer - log_denom

def associations(words, n=10, beam=50):
    possibilities = set()
    words = [alphanumeric_only(w) for w in words]
    for word in words:
        query = DB.relations.find(
          {'rel': {'$in': ['can_adjoin', 'clued_by', 'bigram']},
           'words': word}
        )
        for match in query[:beam]:
            for word2 in match['words']:
                if word != word2 and word2 not in possibilities:
                    possibilities.add(word2)
    results = {}
    for word2 in possibilities:
        match_goodness = 0.0
        for word in words:
            best = 0.0
            for rel in ['can_adjoin', 'clued_by', 'bigram']:
                best = max(best, relation_goodness(rel, word, word2))
            match_goodness += best
        results[word2] = match_goodness
    best_results = sorted(results.items(), key=lambda x: -x[1])
    return best_results[:n]
