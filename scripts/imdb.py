from __future__ import with_statement

import re, math
import itertools

from wordlist_util import strip, normalize

rating_re = re.compile('\s+\S+\s+(\d+)\s+\S+\s+(.+)')
title_re = re.compile('(.[^(]*(?<! ))')
actor_name_re = re.compile('([^\t]*)\t+(.*?)  ')
actor_pos_re = re.compile('<(\d+)>')
actor_rev_re = re.compile('([^,\t(]+),?([^\t(]*)')
aka_title_re = re.compile('(\S[^(]*\(\d+\)(?<! ))')
aka_re = re.compile('   \(aka ([^(]*(?<! ))')

ratings = {}
actor_list = []

def strip_movie_modifiers(t):
    return title_re.match(t).groups()[0]

def strip_actor_modifiers(t):
    last, first = actor_rev_re.match(t).groups()
    return '%s %s'%(first,last)

def is_tv(t):
    return t.find('"')<0

def normalize_title(t):
    t = strip_movie_modifiers(t)
    t = strip(t)
    return t

def normalize_actor(t):
    try:
        t = strip_actor_modifiers(t)
        t = strip(t)
    except:
        print repr(t)
    return t

usa_short_re = re.compile('\(USA\) \(short title\)')
usa_re = re.compile('\(USA\)$')

def aka_is_useful(t):
    if t.find('{')>=0:
        return False
    return bool(
        usa_short_re.search(t) or
        usa_re.search(t)
    )

def load_movies():
    with open(PATH+'/ratings.list','r') as ratings_file:
        for lx in ratings_file:
            if lx=='MOVIE RATINGS REPORT\n':
                break
        for lx in ratings_file:
            l = lx.decode('Latin-1')
            m = rating_re.match(l)
            if m:
                r, title = m.groups()
                rat = int(r)
                ntitle = normalize_title(title)
                if rat>=100:
                    ratings[title] = rat

def do_movies():
    #akas are not guaranteed to be unique so don't stick them in a dictionary
    akas = []
    with open(PATH+'/aka-titles.list','r') as aka_file:
        rat = 0
        for lx in aka_file:
            l = lx.decode('Latin-1')
            m = aka_title_re.match(l)
            if m:
                t = m.groups()[0]
                rat = ratings.get(t,0)
                #print repr(t), rat
            elif rat and aka_is_useful(l):
                try:
                    m = aka_re.match(l)
                    alt = m.groups()[0]
                    akas.append((alt,rat))
                except AttributeError:
                    # for some reason there is one movie that has a parenthesis in its title
                    pass
    allitems = itertools.chain(ratings.iteritems(),akas)
    for t, r in normalize(allitems,normalize_title,4000):
        print "%s,%d"%(t,r)

def parse_actors(actors):
    actor = ''
    for lx in actors:
        l = lx.decode('Latin-1')
        m = actor_name_re.match(l)
        if m:
            ac, title = m.groups()
            if ac:
                actor = ac
            if not title in ratings:
                continue
            m = actor_pos_re.search(l)
            if m:
                p, = m.groups()
                pos = int(p)-2
                if pos<0:
                    pos=0
                weight = int(ratings[title]*math.exp(-.2*pos))
                actor_list.append((actor,weight))

def do_actors():
    with open(PATH+'/actors.list','r') as actors:
        parse_actors(actors)
    with open(PATH+'/actresses.list','r') as actresses:
        parse_actors(actresses)
    for t, r in normalize(actor_list,normalize_actor,6000):
        print "%s,%d"%(t,r)

import sys

def usage():
    sys.stderr.write("usage: imdb.py path list\nwhere list is either 'actors' or 'movies'")
    sys.exit(64)

if __name__=='__main__':
    if len(sys.argv)!=3:
        usage()
    global PATH
    PATH = sys.argv[1]
    if sys.argv[2]=='actors':
        load_movies()
        do_actors()
    elif sys.argv[2]=='movies':
        load_movies()
        do_movies()
    else:
        usage()

