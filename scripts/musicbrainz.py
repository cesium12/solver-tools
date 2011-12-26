"""
A script for generating lists of music artists, albums, and tracks from the Musicbrainz
database.

The database can be downloaded from http://musicbrainz.org/doc/Database_Download.  Both
the core and derived data are required.

The database schema can be found at:
http://svn.musicbrainz.org/mb_server/branches/RELEASE_20090524-BRANCH/admin/sql/CreateTables.sql
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

def do_albums_count():

    names = {}
    counts = {}

    with open(CORE_PATH+'/album','r') as album:
        s = album.readline()
        while(s):
            ss = s.split('\t')
            uid = int(ss[0])
            name = strip(ss[2])
            names[uid] = name
            s = album.readline()
    
    
    with open(DERIVED_PATH+'/albummeta','r') as albummeta:
        s = albummeta.readline()
        while(s):
            ss = s.split('\t')
            try:
                uid = int(ss[0])
                name = names[uid]
                count = (int(ss[3])*10)/int(ss[1])
                counts[name] = counts.get(name,0) + count
            except ZeroDivisionError:
                pass
            s = albummeta.readline()

    with sys.stdout as album_out:
        items = [(name,count) for (name,count) in counts.iteritems() if name and count>=18]
        items.sort(key=lambda x: -x[1])
        for name, count in items:
            album_out.write('%s,%d\n'%(name,count))

def do_artists_count():

    artist_id = {}
    artist_trackid = {}
    counts = {}
    
    with open(CORE_PATH+'/artist','r') as artist:
        s = artist.readline()
        while(s):
            ss = s.split('\t')
            aid = int(ss[0])
            name = strip(ss[1])
            artist_id[aid] = name
            s = artist.readline()
  

    with open(CORE_PATH+'/track','r') as track:
        s = track.readline()
        while(s):
            ss = s.split('\t')
            tid = int(ss[0])
            aid = int(ss[1])
            artist_trackid[tid] = artist_id[aid]
            s = track.readline()

    with open(CORE_PATH+'/puidjoin','r') as puidjoin:
        s = puidjoin.readline()
        while(s):
            ss = s.split('\t')
            tid = int(ss[2])
            name = artist_trackid[tid]
            counts[name] = counts.get(name,0)+1
            s = puidjoin.readline()
    
    with sys.stdout as artist_out:
        items = [(name,count) for (name,count) in counts.iteritems() if name and count>=20]
        items.sort(key=lambda x: -x[1])
        for name, count in items:
            artist_out.write("%s,%d\n" % (name,count))

def do_tracks_count():

    names = {}
    counts = {}

    with open(CORE_PATH+'/track','r') as track:
        s = track.readline()
        while(s):
            ss = s.split('\t')
            aid = int(ss[0])
            name = strip(ss[2])
            names[aid] = name
            s = track.readline()

    with open(CORE_PATH+'/puidjoin','r') as puidjoin:
        s = puidjoin.readline()
        while(s):
            ss = s.split('\t')
            aid = int(ss[2])
            name = names[aid]
            counts[name] = counts.get(name,0)+1
            s = puidjoin.readline()
    
    with sys.stdout as track_out:
        items = [(name,count) for (name,count) in counts.iteritems() if name and count>=6]
        items.sort(key=lambda x: -x[1])
        for name, count in items:
            track_out.write("%s,%d\n"%(name,count))

def usage():
    sys.stderr.write("usage: musicbrainz.py core_data_path [derived_data_path] list\nwhere list is either 'artists', 'albums', or 'tracks'\n")
    sys.exit(64)

if __name__ == '__main__':
    if len(sys.argv)<3 or len(sys.argv)>4:
        usage()
    global CORE_PATH, DERIVED_PATH
    CORE_PATH=sys.argv[1]
    DERIVED_PATH=sys.argv[-2]
    if sys.argv[-1]=='artists':
        do_artists_count()
    elif sys.argv[-1]=='albums':
        do_albums_count()
    elif sys.argv[-1]=='tracks':
        do_tracks_count()
    else:
        usage()

