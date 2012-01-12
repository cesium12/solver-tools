# -*- coding: utf-8 -*-
"""
Usage example::

    from solvertools.wiki.editgrid import *
    grid = EditGrid('editgridtest')
    print grid

The result is a PuzzleArray, similar to a numpy array. You may need to trim
off excess rows and columns, such as by taking grid[:10, :4] to get the first
10 rows and 4 columns.
"""

from solvertools.config import EDITGRID
from solvertools.puzzle_array import PuzzleArray, Header
import urllib2
from urllib import urlencode
import re
import csv
import base64
import xml.dom.minidom as dom

__all__ = ('EditGrid',)

API_URL = 'http://www.editgrid.com/api/v1/rpc'
LOGIN_POST = { 'appKey' : EDITGRID['APP_KEY'],
                 'user' : EDITGRID['USERNAME'],
             'password' : EDITGRID['PASSWORD'],
             'infinite' : 1,
                    'm' : 'auth.createSessionKey' }
DATA_POST = { 'type' : 'csv' }
WORKBOOK_BASENAME = EDITGRID['WORKSPACE'] + '/'

def xml_text(post, tag):
    return dom.parse(urllib2.urlopen(API_URL, urlencode(post))).getElementsByTagName(tag)[0].firstChild.nodeValue

def grid_login():
    DATA_POST['s'] = xml_text(LOGIN_POST, 'value')

def grid_data(name):
    return base64.b64decode(xml_text(dict(DATA_POST, workbook=name, m='workbook.export'), 'base64bin'))

def grid_update(name, data):
    data = '<binary><base64bin>%s</base64bin></binary>' % base64.b64encode(data)
    urllib2.urlopen(API_URL, urlencode(dict(DATA_POST, workbook=name, m='workbook.import', b=data)))

def strip_name(name):
    return re.sub('[^a-zA-Z]', '', name)

def EditGrid(name, header=True):
    data = list(csv.reader(grid_data(WORKBOOK_BASENAME + name).rstrip().split('\n')))
    if header:
        data[0] = [Header(entry) for entry in data[0]]
    for row in data:
        for index in xrange(len(row)):
            if not row[index]:
                row[index] = '/.+/'
    return PuzzleArray(data)

grid_login()
