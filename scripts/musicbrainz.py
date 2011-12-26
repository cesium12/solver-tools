"""
A script for generating lists of music artists, albums, and tracks from the Musicbrainz
database.

The database can be downloaded from http://musicbrainz.org/doc/Database_Download.  Only
the core data is needed.

The database schema can be found at:
http://git.musicbrainz.org/gitweb/?p=musicbrainz-server.git;a=blob;f=admin/sql/CreateTables.sql
"""

# TODO: sort output, better ranking for artists

from __future__ import with_statement

import re, sys, solvertools.util

ex1 = re.compile('[^0-9A-Za-z ]')
ex2 = re.compile('\s+')
ex3 = re.compile('DISC[\d\s]+$')

def strip(s):
    s = solvertools.util.asciify(s)
    s = ex1.sub('',s)
    s = ex2.sub(' ',s)
    s = s.upper()
    s = ex3.sub('',s)
    s = s.strip()
    return s

def lazy_readline(filename):
    with open(filename,'r') as f:
        s = f.readline()
        while(s):
            yield s.split('\t')
            s = f.readline()

def do_albums_count():
   
    release_name = {}
    release_group = {}
    release = {}
    medium = {}
    counts = {}

    for ss in lazy_readline(CORE_PATH+'/release_name'):
        rid = int(ss[0])
        name = strip(ss[1])
        release_name[rid] = name

    for ss in lazy_readline(CORE_PATH+'/release_group'):
        try:
            rt = int(ss[4])
            if rt in [1,3,4,5,9]:
                rgid = int(ss[0])
                rid = int(ss[2])
                release_group[rgid]=release_name[rid]
        except ValueError:
            pass

    del release_name

    for ss in lazy_readline(CORE_PATH+'/release'):
        rgid = int(ss[4])
        rid = int(ss[0])
        try:
            release[rid]=release_group[rgid]
        except KeyError:
            pass

    del release_group

    for ss in lazy_readline(CORE_PATH+'/medium'):
        rid = int(ss[2])
        mid = int(ss[0])
        try:
            medium[mid] = release[rid]
        except KeyError:
            pass

    del release

    for ss in lazy_readline(CORE_PATH+'/medium_cdtoc'):
        mid = int(ss[1])
        try:
            name = medium[mid]
            counts[name] = counts.get(name,0)+1
        except KeyError:
            pass

    del medium

    items = [(name,count) for (name,count) in counts.iteritems() if name and count>=2]
    items.sort(key=lambda x: -x[1])
    for name, count in items:
        sys.stdout.write("%s,%d\n"%(name,count))

def do_artists_count():

    artist_names = {}
    credit_names = {}
    recording_names = {}
    counts = {}

    for ss in lazy_readline(CORE_PATH+'/artist_name'):
        aid = int(ss[0])
        name = strip(ss[1])
        artist_names[aid] = name

    for ss in lazy_readline(CORE_PATH+'/artist_credit'): 
        cid = int(ss[0])
        aid = int(ss[1])
        credit_names[cid] = artist_names[aid]

    del artist_names

    for ss in lazy_readline(CORE_PATH+'/recording'):
        rid = int(ss[0])
        cid = int(ss[3])
        recording_names[rid] = credit_names[cid]

    del credit_names

    for ss in lazy_readline(CORE_PATH+'/recording_puid'):
        rid = int(ss[2])
        name = recording_names[rid]
        counts[name]=counts.get(name,0)+1

    del recording_names

    items = [(name,count) for (name,count) in counts.iteritems() if name and count>=6]
    items.sort(key=lambda x: -x[1])
    for name, count in items:
        sys.stdout.write("%s,%d\n"%(name,count))

def do_tracks_count():

    track_names = {}
    recording_names = {}
    counts = {}

    for ss in lazy_readline(CORE_PATH+'/track_name'):
        nid = int(ss[0])
        name = strip(ss[1])
        track_names[nid] = name

    for ss in lazy_readline(CORE_PATH+'/recording'):
        rid = int(ss[0])
        nid = int(ss[2])
        recording_names[rid] = track_names[nid]

    del track_names

    for ss in lazy_readline(CORE_PATH+'/recording_puid'):
        rid = int(ss[2])
        name = recording_names[rid]
        counts[name]=counts.get(name,0)+1

    del recording_names

    items = [(name,count) for (name,count) in counts.iteritems() if name and count>=6]
    items.sort(key=lambda x: -x[1])
    for name, count in items:
        sys.stdout.write("%s,%d\n"%(name,count))

def usage():
    sys.stderr.write("usage: musicbrainz.py core_data_path list\nwhere list is either 'artists', 'albums', or 'tracks'\n")
    sys.exit(64)

if __name__ == '__main__':
    if len(sys.argv)!=3:
        usage()
    global CORE_PATH, DERIVED_PATH
    CORE_PATH=sys.argv[1]
    if sys.argv[2]=='artists':
        do_artists_count()
    elif sys.argv[2]=='albums':
        do_albums_count()
    elif sys.argv[2]=='tracks':
        do_tracks_count()
    else:
        usage()

