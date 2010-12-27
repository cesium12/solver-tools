import re, solvertools.util

alnumspace = re.compile('[^0-9A-Za-z ]')
spaces = re.compile('\s+')

def strip(s):
    s = solvertools.util.asciify(s)
    s = alnumspace.sub('',s)
    s = spaces.sub(' ',s)
    s = s.upper()
    s = s.strip()
    return s

def normalize(items, func=strip, min=0):
    d = {}
    for (k,v) in items:
        nk = func(k)
        d[nk] = d.get(nk,0) + v
    items = filter(lambda x: x[1] >= min, d.iteritems())
    items.sort(key=lambda x: -x[1])
    return items
