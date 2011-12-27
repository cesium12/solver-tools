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

ex_track = re.compile('TRACK \d+')

# release group types
RG_ALBUM = 1
RG_EP = 3
RG_COMPILATION = 4
RG_SOUNDTRACK = 5
RG_LIVE = 9

def invalid_artist(s):
    return (not s) or (s=='UNKNOWN')

def invalid_track(s):
    return (not s) or (s=='UNTITLED') or ex_track.match(s)

def invalid_album(s):
    return (not s)

def strip(s):
    s = solvertools.util.asciify(s)
    s = s.replace('&','AND')
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

def get_artist_credit_names():

    artist_names = {}
    credit_names = {}
   
    for ss in lazy_readline(CORE_PATH+'/artist_name'):
        aid = int(ss[0])
        name = strip(ss[1])
        if not invalid_artist(name):
            artist_names[aid] = name

    for ss in lazy_readline(CORE_PATH+'/artist_credit'): 
        cid = int(ss[0])
        aid = int(ss[1])
        try:
            credit_names[cid] = artist_names[aid]
        except KeyError:
            pass

    return credit_names

def get_release_group(types):

    release_name = {}
    release_group = {}

    for ss in lazy_readline(CORE_PATH+'/release_name'):
        rid = int(ss[0])
        name = strip(ss[1])
        if not invalid_album(name):
            release_name[rid] = name

    for ss in lazy_readline(CORE_PATH+'/release_group'):
        try:
            rt = int(ss[4])
        except ValueError:
            continue
        if rt not in types:
            continue
        rgid = int(ss[0])
        rid = int(ss[2])
        try:
            name = release_name[rid]
        except KeyError:
            continue
        release_group[rgid]=name

    return release_group

def get_release(types):

    release = {}
    release_group = get_release_group(types)

    for ss in lazy_readline(CORE_PATH+'/release'):
        rgid = int(ss[4])
        rid = int(ss[0])
        try:
            release[rid]=release_group[rgid]
        except KeyError:
            pass

    return release

def get_counts_from_release(release):
  
    medium = {}
    counts = {}

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

    return counts

def get_track_names():

    track_names = {}

    for ss in lazy_readline(CORE_PATH+'/track_name'):
        nid = int(ss[0])
        name = strip(ss[1])
        if not invalid_track(name):
            track_names[nid] = name

    return track_names

def output_three(counts,min_count):
    
    items = [(artist,track,count) for ((artist,track),count) in counts.iteritems() if count>=min_count]
    items.sort(key=lambda x: -x[2])
    for artist, track, count in items:
        sys.stdout.write("%s\t%s\t%d\n"%(artist,track,count))

def do_albums_count():

    counts = {}
    medium = {}

    release = get_release([RG_ALBUM,RG_EP,RG_COMPILATION,RG_SOUNDTRACK,RG_LIVE])
    
    counts = get_counts_from_release(release)
  
    items = [(name,count) for (name,count) in counts.iteritems() if name and count>=2]
    items.sort(key=lambda x: -x[1])
    for name, count in items:
        sys.stdout.write("%s,%d\n"%(name,count))

def do_artists_count():

    recording_names = {}
    counts = {}

    credit_names = get_artist_credit_names()

    for ss in lazy_readline(CORE_PATH+'/recording'):
        rid = int(ss[0])
        cid = int(ss[3])
        try:
            recording_names[rid] = credit_names[cid]
        except KeyError:
            pass

    del credit_names

    for ss in lazy_readline(CORE_PATH+'/recording_puid'):
        rid = int(ss[2])
        try:
            name = recording_names[rid]
        except KeyError:
            continue
        counts[name]=counts.get(name,0)+1

    del recording_names

    items = [(name,count) for (name,count) in counts.iteritems() if name and count>=6]
    items.sort(key=lambda x: -x[1])
    for name, count in items:
        sys.stdout.write("%s,%d\n"%(name,count))

def do_tracks_count():

    recording_names = {}
    counts = {}

    track_names = get_track_names()

    for ss in lazy_readline(CORE_PATH+'/recording'):
        rid = int(ss[0])
        nid = int(ss[2])
        try:
            recording_names[rid] = track_names[nid]
        except KeyError:
            pass

    del track_names

    for ss in lazy_readline(CORE_PATH+'/recording_puid'):
        rid = int(ss[2])
        try:
            name = recording_names[rid]
        except KeyError:
            continue
        counts[name]=counts.get(name,0)+1

    del recording_names

    items = [(name,count) for (name,count) in counts.iteritems() if name and count>=6]
    items.sort(key=lambda x: -x[1])
    for name, count in items:
        sys.stdout.write("%s,%d\n"%(name,count))

def do_artist_track_rel():

    recording_names = {}
    counts = {}

    credit_names = get_artist_credit_names()

    track_names = get_track_names()

    for ss in lazy_readline(CORE_PATH+'/recording'):
        rid = int(ss[0])
        tid = int(ss[2])
        cid = int(ss[3])
        try:
            recording_names[rid] = (credit_names[cid], track_names[tid])
        except KeyError:
            pass

    del credit_names, track_names

    for ss in lazy_readline(CORE_PATH+'/recording_puid'):
        rid = int(ss[2])
        try:
            name = recording_names[rid]
        except KeyError:
            continue
        counts[name]=counts.get(name,0)+1

    del recording_names

    output_three(counts,15)
   
def do_album_track_rel():

    tracklist = {}
    track = {}
    counts = {}

    release = get_release([RG_ALBUM,RG_EP,RG_SOUNDTRACK,RG_LIVE])

    for ss in lazy_readline(CORE_PATH+'/medium'):
        tid = int(ss[1])
        rid = int(ss[2])
        try:
            tracklist[tid] = release[rid]
        except KeyError:
            pass

    track_name = get_track_names()

    for ss in lazy_readline(CORE_PATH+'/track'):
        rid = int(ss[1])
        tid = int(ss[2])
        nid = int(ss[4])
        try:
            aname = tracklist[tid]
            tname = track_name[nid]
        except KeyError:
            continue
        track[rid] = (aname,tname)

    del tracklist, track_name

    for ss in lazy_readline(CORE_PATH+'/recording_puid'):
        rid = int(ss[2])
        try:
            name = track[rid]
        except KeyError:
            continue
        counts[name]=counts.get(name,0)+1

    output_three(counts,10)

def do_artist_album_rel():

    counts = {}
    release = {}
    
    artist_credit = get_artist_credit_names()
    release_group = get_release_group([RG_ALBUM,RG_EP,RG_COMPILATION,RG_SOUNDTRACK,RG_LIVE])

    for ss in lazy_readline(CORE_PATH+'/release'):
        rgid = int(ss[4])
        rid = int(ss[0])
        aid = int(ss[3])
        try:
            release[rid]=(artist_credit[aid],release_group[rgid])
        except KeyError:
            pass

    del artist_credit, release_group

    counts = get_counts_from_release(release)

    del release

    output_three(counts,5)

def usage():
    sys.stderr.write("usage: musicbrainz.py core_data_path list\nwhere list is one of:\n")
    for k in sorted(commands):
        sys.stderr.write('\t')
        sys.stderr.write(k)
        sys.stderr.write('\n')
    sys.exit(64)

commands = {
    'artists' : do_artists_count,
    'albums' : do_albums_count,
    'tracks' : do_tracks_count,
    'artist-track' : do_artist_track_rel,
    'album-track' : do_album_track_rel,
    'artist-album' : do_artist_album_rel,
}

if __name__ == '__main__':
    if len(sys.argv)!=3:
        usage()
    global CORE_PATH
    CORE_PATH=sys.argv[1]
    commands.get(sys.argv[2],usage)()

