from model.language_model import english_model
from string import lowercase
from collections import defaultdict
from random import shuffle, random
import math

def make_pattern(word):
    # word must be all lowercase with no punctuation
    letters = []
    pattern = []
    for ch in word:
        if ch in letters:
            pattern.append(letters.index(ch))
        else:
            pattern.append(len(letters))
            letters.append(ch)
    return tuple(pattern)

patterns = defaultdict(list)
#for word in english_model.all_words():
for word in open('../model/dict/enable.txt'):
    word = word.strip()
    word = ''.join(let.lower() for let in word if let.lower() in lowercase)
    pattern = make_pattern(word)
    patterns[pattern].append(word)
patterns[(0,)].append('a')
patterns[(0,)].append('i')

print patterns[0,1,2,3,4,5,0,4]
print patterns[0,1,2,0,3,4,0,4]

def smash_words(text):
    return ''.join(ch for ch in text.lower() if ch in lowercase+' ')

def possible_substitutions(cryptword):
    pattern = make_pattern(cryptword)
    for word in patterns[pattern]:
        # no longer + len(word)
        val = math.pow(2, english_model.words_logprob([word]) + len(word)/2)
        yield val, zip(cryptword, word)

def text_substitutions(ciphertext, good_words=[]):
    ciphertext = smash_words(ciphertext.replace('-', ' '))
    possible = defaultdict(float)
    for word in ciphertext.split():
        pattern = make_pattern(word)
        for value, sub in possible_substitutions(word):
            possible[tuple(sub)] += value
        for gword in good_words:
            if make_pattern(gword) == pattern:
                possible[tuple(zip(word, gword))] += 8
    items = sorted(possible.items(), key=lambda x: -x[1])
    return [item[0] for item in items]

def decrypt(text, decryptdict):
    return ''.join((decryptdict[ch] if ch in lowercase else ch)
                   for ch in text)

def crypto_solve(text, hints=[]):
    text = text.lower()
    counts = defaultdict(int)
    for ch in lowercase: counts[ch] += 1
    for ch in text:
        if ch in lowercase: counts[ch] += 1
    disordered = list(lowercase)
    shuffle(disordered)
    decryptdict = {}
    encryptdict = {}

    for cipher, plain in zip(lowercase, disordered):
        decryptdict[cipher[0]] = plain[0]
        encryptdict[plain[0]] = cipher[0]
    subs = text_substitutions(text, hints)
    print len(subs)
    while True:
        result = decrypt(text, decryptdict)
        likelihood = english_model.text_logprob(result)
        print likelihood, result
        best_likelihood = likelihood
        best_dicts = None
        switched = False
        for sub in subs:
            newdecrypt = dict(decryptdict)
            newencrypt = dict(encryptdict)
            for c, p in sub:
                c2 = newencrypt[p]
                p2 = newdecrypt[c]
                newdecrypt[c] = p
                newencrypt[p] = c
                newdecrypt[c2] = p2
                newencrypt[p2] = c2
            tried = decrypt(text, newdecrypt)
            tried_likelihood = english_model.text_logprob(tried)
            if (tried_likelihood > best_likelihood):
                decryptdict, encryptdict = (newdecrypt, newencrypt)
                switched = True
                break
        if not switched:
            return result

def demo():
    print crypto_solve("""
    WDF HWFK L HFLX IJET ETF HFSWD: L EFD-MLBZ WQ NXLDZ QXWMMJFK QWP TJK KWYX.
    -- DFJX RLJSLD
    """)
    print crypto_solve("""
    XKG DVXA XKNX KNB TDDOWVGB PGQN DNJNNJ RNQ JTR PNLDKVJZ NDLTQQ XKG WHNVJ.
    -- ZLGZ UGNL
    """)
    print crypto_solve("""AE ZDWUB'E WBZ CAEM DBW---AE IWRABU CAEM X CMASYWT.
    -- T. X. HXOOWTEF""")
    print crypto_solve("""
    SGKDK BDK SIR IBLP SR SKOO B IMFBDV.
    -- SKDDL QMPPRA
    """)
    print crypto_solve("""
    HECQHVCFMO FMIX, AMKCFKCY M UEPOS, LEP WPVMFQPVI RMOL MC KCWR FMOO.
    -- LPVSPKW DPEUC
    """)

if __name__ == '__main__': demo()

