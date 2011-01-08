# -*- coding: utf-8 -*-
"""
Usage:
>>> from solvertools.wiki.editgrid import *
>>> print EditGrid('editgridtest')
FALSE                ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890
Testing.d            abcdefghijklmnopqrstuvwxyz          
Testing. from a wii  ~!@#$%^&*()_+`-={}|[]\:";'<>?,./    
mii too! :D          KMUVXY78#&                          
Testing.                                                 
Testing.                                                 
Testing.                                                 
Testing.                                                 
Testing.                                                 
test!
"""

from solvertools.config import EDITGRID
from solvertools.puzzle_array import PuzzleArray
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

def EditGrid(name):
    return PuzzleArray(list(csv.reader(grid_data(WORKBOOK_BASENAME + name).rstrip().split('\n'))))

grid_login()
