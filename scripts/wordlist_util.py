import re, solvertools.util, sys

separator = re.compile('[/]+')
alnumspace = re.compile('[^0-9A-Za-z ]')
spaces = re.compile('\s+')

def strip(s):
    s = solvertools.util.asciify(s)
    s = s.replace('&','AND')
    s = separator.sub(' ',s)
    s = alnumspace.sub('',s)
    s = spaces.sub(' ',s)
    s = s.upper()
    s = s.strip()
    return s

def output_wordlist(counts,min_count=0):
    items = [(name,count) for (name,count) in counts.iteritems() if count>=min_count]
    items.sort(key=lambda x: -x[1])
    for item in items:
        sys.stdout.write("%s,%d\n"%item)

def output_relation(counts,min_count=0):
    items = [(name1,name2,count) for ((name1,name2),count) in counts.iteritems() if count>=min_count]
    items.sort(key=lambda x: -x[2])
    for item in items:
        sys.stdout.write("%s\t%s\t%d\n"%item)

def normalize(items, func=strip, min=0):
    d = {}
    for (k,v) in items:
        nk = func(k)
        d[nk] = d.get(nk,0) + v
    items = filter(lambda x: x[1] >= min, d.iteritems())
    items.sort(key=lambda x: -x[1])
    return items
