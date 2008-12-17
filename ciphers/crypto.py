from model.language_model import english_model, valid_chars, scan_ngrams
from model.blanks import ngram_blanks
from string import lowercase
from collections import defaultdict
from heapq import heappush, heappop
from random import shuffle, random
import math, re

unigram = english_model.word_dist[1]

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
for word in english_model.all_words():
    word = english_model.convert(word)
    pattern = make_pattern(word)
    patterns[pattern].append(word)

def smash_words(text):
    return ''.join(ch for ch in text.lower() if ch in lowercase+' ')

def eval_ngrams(text):
    logprob = 0
    for word in text.split():
        for n in (1, 2, 3):
            for ngram in scan_ngrams(word, n):
                dots = ngram.count('.')
                logprob += ngram_blanks[n][ngram] - 4.7*dots
    return logprob/len(text)

def possible_substitutions(cryptword):
    pattern = make_pattern(cryptword)
    for word in patterns[pattern]:
        val = unigram.logprob((word,)) + len(word)
        yield val, zip(cryptword, word)

def text_substitutions(ciphertext):
    ciphertext = smash_words(ciphertext.replace('-', ' '))
    possible = defaultdict(float)
    for word in ciphertext.split():
        pattern = make_pattern(word)
        for value, sub in possible_substitutions(word):
            possible[tuple(sub)] = value
    items = sorted(possible.items(), key=lambda x: -x[1])
    return [item[0] for item in items]

memo = {}
def eval_text(text, patternlist):
    tot_logprob = 0
    for frame, pattern in zip(text.split(), patternlist):
        if (frame, pattern) in memo:
            tot_logprob += memo[(frame, pattern)]
        else:
            wordprob = 1e-9
            regex = re.compile(frame)
            for word in patterns[pattern]:
                if regex.match(word):
                    wordprob += unigram.prob((word,))
            logprob = math.log(wordprob)
            memo[(frame, pattern)] = logprob
            tot_logprob += logprob
    return tot_logprob + eval_ngrams(text)


def decrypt(text, decryptdict):
    return ''.join((decryptdict[ch] if ch in lowercase else ch)
                   for ch in text)

def crypto_solve(text):
    text = english_model.convert(text)
    patternlist = [make_pattern(x) for x in text.split()]

    q = [(10000, '..........................')]
    already = set()
    subs = text_substitutions(text)

    while q:
        decryptdict = {}
        encryptdict = {}
        score, trans = heappop(q)
        unknown_in = set()
        unknown_out = set(lowercase)
        for c1, c2 in zip(lowercase, trans):
            decryptdict[c1] = c2
            encryptdict[c2] = c1
            if c2 == '.':
                if c1 in text: unknown_in.add(c1)
            else: unknown_out.remove(c2)

        result = decrypt(text, decryptdict)
        print score, result
        if len(unknown_in) == 0: return result

        for sub in subs:
            newdecrypt = dict(decryptdict)
            newencrypt = dict(encryptdict)
            for c, p in sub:
                if p in newencrypt:
                    c2 = newencrypt[p]
                    decryptdict[c2] = '.'
                if newdecrypt[c] != '.':
                    p2 = newdecrypt[c]
                    del newencrypt[p2]
                newdecrypt[c] = p
                newencrypt[p] = c

            tried = decrypt(text, newdecrypt)
            triedprob = eval_text(tried, patternlist) - 10*len(unknown_in)
            newtrans = ''.join(newdecrypt[x] for x in lowercase)
            entry = (-triedprob, newtrans)
            if newtrans not in already:
                heappush(q, entry)
                already.add(newtrans)

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

