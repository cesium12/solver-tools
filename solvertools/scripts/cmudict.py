# -*- coding: utf-8 -*-
import string
import codecs
from solvertools.util import get_dictfile
from collections import defaultdict

# Note: These vowel equivalents are linguistically inaccurate, lumping together
# many sounds that are actually different but sound basically the same to
# most American English speakers. That's fine, because Mystery Hunt puzzle
# writers do exactly the same thing.
#
# Also, we basically have to do this, because CMU already smashed together
# things that are the same when pronounced with a Pittsburgh accent, or just
# guessed wrong about some pronunciations.
#
# Anyway. This representation pretends that there are the following nine
# monophthongs in English (following a sort of continuum):
#
# u ʊ o ə a æ e ɪ i

CMU_PHONEMES = {
   'AA': u'a',
   'AE': u'æ',
   'AH': u'ə',
   'AW': u'aʊ',
   'AY': u'aɪ',
   'EH': u'e',
   'ER': u'ər',
   'EY': u'eɪ',
   'IH': u'ɪ',
   'IY': u'i',
   'AO': u'o',
   'OW': u'oʊ',
   'OY': u'oɪ',
   'UH': u'ʊ',
   'UW': u'u',
   'W': u'w',
   'Y': u'j',
   
   'B': u'b',
   'CH': u'tʃ',
   'D': u'd',
   'DH': u'ð',
   'F': u'f',
   'G': u'g',
   'HH': u'h',
   'JH': u'dʒ',
   'K': u'k',
   'L': u'l',
   'M': u'm',
   'N': u'n',
   'NG': u'ŋ',
   'P': u'p',
   'R': u'r',
   'S': u's',
   'SH': u'ʃ',
   'T': u't',
   'TH': u'θ',
   'V': u'v',
   'Z': u'z',
   'ZH': u'ʒ',
}

def translate_cmu_phoneme(s):
    if s[-1] in string.digits:
        phon = CMU_PHONEMES[s[:-1]]
        if s[-1] == '1':
            return u"'" + phon
        else:
            return phon
    else:
        return CMU_PHONEMES[s]

def translate_cmu_phonetics(s):
    phonemes = s.split()
    return u''.join(translate_cmu_phoneme(phon) for phon in phonemes)

def translate_cmu_entry(entry):
    text, phonemes = entry.split('  ')
    if len(text) > 3 and text[-3] == '(' and text[-1] == ')':
        # secondary entry
        text = text[:-3]
    phonetic = translate_cmu_phonetics(phonemes)
    text = text.replace('-', '')
    return text, phonetic

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
        phon = u'|'.join(phondict[word])
        print >> outfile, u"%s,%s" % (word, phon)
        print u"%s,%s" % (word, phon)
    outfile.close()

if __name__ == '__main__':
    make_dict()
