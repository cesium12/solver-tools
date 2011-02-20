"""
A script for generating lists of music artists, albums, and tracks from the Musicbrainz
database.

The database can be downloaded from http://musicbrainz.org/doc/Database_Download.  Both
the core and derived data are required.

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

def do_albums():

    allowed_albums = set()

    with open(DERIVED_PATH+'/albummeta','r') as albummeta:
        s = albummeta.readline()
        while(s):
            ss = s.split('\t')
            if 3*int(ss[3])>4*int(ss[1]):
                allowed_albums.add(int(ss[0]))
            s = albummeta.readline()

    with open(CORE_PATH+'/album','r') as album:
        with sys.stdout as album_out:
            s = album.readline()
            while(s):
                ss = s.split('\t')
                if int(ss[0]) in allowed_albums:
                    name = strip(ss[2])
                    album_out.write(name)
                    album_out.write('\n')
                s = album.readline()

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
        for name, count in counts.iteritems():
            if count >= 18 and name:
                album_out.write('%s,%d\n'%(name,count))

def do_artists():

    tags = {}

    with open(DERIVED_PATH+'/artist_tag','r') as artist_tag:
        s = artist_tag.readline()
        while(s):
            ss = s.split('\t')
            aid = int(ss[0])
            count = int(ss[2])
            tags[aid] = tags.get(aid,0)+count
            s = artist_tag.readline()

    with open(CORE_PATH+'/artist','r') as artist:
        with open('data/dict/musicbrainz_artists_u.txt','w') as artist_out:
            s = artist.readline()
            while(s):
                ss = s.split('\t')
                aid = int(ss[0])
                if tags.get(aid,0)>=1:
                    name = strip(ss[1])
                    artist_out.write(name)
                    artist_out.write('\n')
                s = artist.readline()

def do_artists_count():

    names = {}
    counts = {}
    
    with open(CORE_PATH+'/artist','r') as artist:
        s = artist.readline()
        while(s):
            ss = s.split('\t')
            aid = int(ss[0])
            name = strip(ss[1])
            names[aid] = name
            s = artist.readline()
    
    with open(DERIVED_PATH+'/artist_tag','r') as artist_tag:
        s = artist_tag.readline()
        while(s):
            ss = s.split('\t')
            aid = int(ss[0])
            name = names[aid]
            count = int(ss[2])
            counts[name] = counts.get(name,0)+count
            s = artist_tag.readline()

    with sys.stdout as artist_out:
        for name, count in counts.iteritems():
            if name:
                artist_out.write("%s,%d\n" % (name,count))

def do_tracks():

    puids = {}

    with open(CORE_PATH+'/puidjoin','r') as puidjoin:
        s = puidjoin.readline()
        while(s):
            ss = s.split('\t')
            aid = int(ss[2])
            puids[aid] = puids.get(aid,0)+1
            s = puidjoin.readline()

    with open(CORE_PATH+'/track','r') as track:
        with sys.stdout as track_out:
            s = track.readline()
            while(s):
                ss = s.split('\t')
                aid = int(ss[0])
                if puids.get(aid,0)>=3:
                    name = strip(ss[2])
                    track_out.write(name)
                    track_out.write('\n')
                s = track.readline()

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
        for name, count in counts.iteritems():
            if count>=6 and name:
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

