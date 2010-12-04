from nltk.corpus import wordnet
get_synset = wordnet._synset_from_pos_and_offset

def get_adjacent(synset):
    return [name for pointer_tuples in synset._pointers.values() for pos, offset in pointer_tuples for name in get_synset(pos, offset).lemma_names]

def crosswordify(lemma_name):
    return lemma_name.upper().replace("_", "").replace("-", "").replace("'", "").replace(".","")

def make_wordnet_clues():
    synsets = wordnet.all_synsets()
    entries = []
    for syn in synsets:
        names = [crosswordify(name) for name in syn.lemma_names]
        defn = syn.definition
        related = [crosswordify(name) for name in get_adjacent(syn)]
        examples = ", ".join('"%s"' % ex for ex in syn.examples)
        for name in names:
            related2 = [n for n in names if n != name] + related
            entries.append("%s\t%s -- %s -- %s" % (name, defn, examples, 
                                                   ', '.join(related2)))
    entries.sort()
    for entry in entries:
        print entry



if __name__ == '__main__':
    make_wordnet_clues()
