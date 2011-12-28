"""
A script for generating a list of movies and actors from text files
provided by IMDb.

The IMDb text files can be found at http://www.imdb.com/interfaces#plain.
The files that are used by this script are actors, actresses, aka-titles,
and ratings.

Unfortunately the files aren't in the most parser friendly format, so we
need to use regexes a lot.
"""

from __future__ import with_statement

import re, math, sys
import itertools

from wordlist_util import strip, normalize, output_relation, output_wordlist

rating_re = re.compile('\s+\S+\s+(\d+)\s+\S+\s+(.+)')
title_re = re.compile('(.[^(]*(?<! ))')
actor_name_re = re.compile('([^\t]*)\t+(.*?)  ')
actor_role_re = re.compile('\[([^\]]+)\]')
actor_pos_re = re.compile('<(\d+)>')
actor_rev_re = re.compile('([^,\t(]+),?([^\t(]*)')
aka_title_re = re.compile('(\S[^(]*\(\d+\)(?<! ))')
aka_re = re.compile('   \(aka ([^(]*(?<! ))')
self_re = re.compile('HIMSELF|HERSELF|THEMSELVES')

def precompute_exps():
    l = []
    f = math.exp(-.2)
    x = 1
    for i in xrange(75):
        l.append(x)
        x*=f
    return l

exps = precompute_exps()

def weight_factor(pos):
    if pos<75:
        return exps[pos]
    else:
        return 0.

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

def normalize_role(t,actor):
    t = strip(t)
    t = self_re.sub(actor,t)
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

def load_movie_ratings():
    ratings = {}

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
                if rat>=100:
                    ratings[title] = rat
    return ratings

def do_movies():
    ratings = load_movie_ratings()
    movies = {}
    for title, rat in ratings.iteritems():
        ntitle = normalize_title(title)
        movies[ntitle] = movies.get(ntitle,0) + rat
    with open(PATH+'/aka-titles.list','r') as aka_file:
        rat = 0
        for lx in aka_file:
            l = lx.decode('Latin-1')
            m = aka_title_re.match(l)
            if m:
                title = m.groups()[0]
                rat = ratings.get(title,0)
            elif rat and aka_is_useful(l):
                try:
                    m = aka_re.match(l)
                    alt = m.groups()[0]
                    ntitle = normalize_title(alt)
                    movies[ntitle] = movies.get(ntitle,0) + rat
                except AttributeError:
                    # for some reason there is one movie that has a parenthesis in its title
                    pass
    output_wordlist(movies,4000)

def parse_actors(actors,ratings,counts):
    actor = ''
    for lx in actors:
        l = lx.decode('Latin-1')
        m = actor_name_re.match(l)
        if m:
            ac, title = m.groups()
            if ac:
                actor = normalize_actor(ac)
            if not title in ratings:
                continue
            m = actor_pos_re.search(l)
            if m:
                p, = m.groups()
                pos = int(p)-1
                weight = int(ratings[title]*weight_factor(pos))
                counts[actor] = counts.get(actor,0) + weight

def parse_actor_roles(actors,ratings,counts):
    actor = ''
    for lx in actors:
        l = lx.decode('Latin-1')
        m = actor_name_re.match(l)
        if m:
            ac, title = m.groups()
            if ac:
                actor = normalize_actor(ac)
            if not title in ratings:
                continue
            mpos = actor_pos_re.search(l)
            mrole = actor_role_re.search(l)
            if mpos and mrole:
                p, = mpos.groups()
                pos = int(p)-1
                weight = int(ratings[title]*weight_factor(pos))
                r, = mrole.groups()
                ntitle = normalize_title(title)
                role = normalize_role(r,actor)
                t = (ntitle,actor,role)
                counts[t] = counts.get(t,0) + weight


def do_actors(keyfunc=lambda a,t: a):
    ratings = load_movie_ratings()
    counts = {}
    keyfunc = lambda a,t : a
    with open(PATH+'/actors.list','r') as actors:
        parse_actors(actors,ratings,counts)
    with open(PATH+'/actresses.list','r') as actresses:
        parse_actors(actresses,ratings,counts)
    output_wordlist(counts,6000)

def do_roles():
    ratings = load_movie_ratings()
    counts = {}
    keyfunc = lambda a,t : (a,normalize_title(t))
    with open(PATH+'/actors.list','r') as actors:
        parse_actor_roles(actors,ratings,counts)
    with open(PATH+'/actresses.list','r') as actresses:
        parse_actor_roles(actresses,ratings,counts)
    items = [(movie,actor,role,count) for ((movie,actor,role),count) in counts.iteritems() if count >= 24000]
    items.sort(key=lambda x: -x[3])
    for item in items:
        sys.stdout.write('%s\t%s\t%s\t%d\n'%item)

def usage():
    sys.stderr.write("usage: imdb.py input_path list\nwhere list is one of:'\n")
    for k in sorted(commands):
        sys.stderr.write('\t')
        sys.stderr.write(k)
        sys.stderr.write('\n')
    sys.exit(64)

commands = {
    'movies' : do_movies,
    'actors' : do_actors,
    'roles' : do_roles
}

if __name__=='__main__':
    if len(sys.argv)!=3:
        usage()
    global PATH
    PATH = sys.argv[1]
    commands.get(sys.argv[2],usage)()
