from model.language_model import english_model, valid_chars, scan_ngrams
from model.blanks import ngram_blanks
from string import lowercase
from collections import defaultdict
from heapq import heappush, heappop
from random import shuffle, random
import math, re

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

memo = {}
def eval_text(text, patternlist):
    tot_logprob = 0
    for frame, pattern in zip(text.split(), patternlist):
        if (frame, pattern) in memo:
            tot_logprob += memo[(frame, pattern)]
        else:
            wordprob = 1e-7
            regex = re.compile(frame)
            for word in patterns[pattern]:
                if regex.match(word):
                    wordprob += english_model.word_dist[1].prob((word,))
            logprob = math.log(wordprob)
            memo[(frame, pattern)] = logprob
            tot_logprob += logprob
    return tot_logprob


def decrypt(text, decryptdict):
    return ''.join((decryptdict[ch] if ch in lowercase else ch)
                   for ch in text)

def crypto_solve(text):
    text = english_model.convert(text)
    patternlist = [make_pattern(x) for x in text.split()]

    q = [(10000, '..........................')]
    already = set()

    while q:
        decryptdict = {}
        score, trans = heappop(q)
        unknown_in = set()
        unknown_out = set(lowercase)
        for c1, c2 in zip(lowercase, trans):
            decryptdict[c1] = c2
            if c2 == '.' and c1 in text: unknown_in.add(c1)
            else: unknown_out.remove(c2)

        result = decrypt(text, decryptdict)
        print score, result
        if len(unknown_in) == 0: return result

        for ci in unknown_in:
            for co in unknown_out:
                decryptdict[ci] = co

                tried = decrypt(text, decryptdict)
                triedprob = eval_text(tried, patternlist) - 10*len(unknown_in)
                newtrans = ''.join(decryptdict[x] for x in lowercase)
                entry = (-triedprob, newtrans)
                if newtrans not in already:
                    heappush(q, entry)
                    already.add(newtrans)

                decryptdict[ci] = '.'

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

