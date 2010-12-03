# -*- coding: utf-8 -*-
import string
import codecs
from solvertools.util import get_dictfile
from solvertools.phonetic.arpabet import arpa_to_ipa
from collections import defaultdict

def translate_cmu_entry(entry):
    text, phonemes = entry.split('  ')
    if len(text) > 3 and text[-3] == '(' and text[-1] == ')':
        # secondary entry
        text = text[:-3]
    phonetic = arpa_to_ipa(phonemes)
    text = text.replace('-', '')
    return text, phonetic

# This transformation is ultimately unnecessary, now that I changed the
# wordlist format. Oh well.

def read_cmu_dict(infile):
    phondict = defaultdict(list)
    for line in infile:
        line = line.strip()
        if line.startswith(';;'):
            continue
        while line[0] not in string.uppercase:
            # trim weird punctuation entries
            line = line[1:]
        if not line: continue
        text, phonetic = translate_cmu_entry(line.strip())
        if phonetic not in phondict[text]:
            phondict[text].append(phonetic)
    return phondict

def make_dict():
    infile = open(get_dictfile('cmudict.0.7a'))
    phondict = read_cmu_dict(infile)
    infile.close()

    outfile = codecs.open(get_dictfile('phonetic.txt'), 'w',
                          encoding='utf-8')
    keys = phondict.keys()
    keys.sort()
    for word in keys:
        for phon in phondict[word]:
            print >> outfile, u"%s,%s" % (word, phon)
            print u"%s,%s" % (word, phon)
    outfile.close()

if __name__ == '__main__':
    make_dict()

