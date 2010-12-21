from pymongo import Connection, ASCENDING, DESCENDING
from solvertools.config import DB_USERNAME, DB_PASSWORD
CONNECTION = Connection('tortoise.csc.media.mit.edu')
DB = CONNECTION.puzzlebase
import logging
logger = logging.getLogger(__name__)
DB.authenticate(DB_USERNAME, DB_PASSWORD)

DB.relations.ensure_index([('words', ASCENDING),
                           ('interestingness', DESCENDING),
                           ('freq', DESCENDING)])

DB.relations.ensure_index([('words', ASCENDING),
                           ('value', ASCENDING),
                           ('interestingness', DESCENDING),
                           ('freq', DESCENDING)])


def add_relation(rel, words, value=None, freq=1):
    # do an upsert on rel, [word1, word2], setting the freq
    return DB.relations.update(
        {'rel': rel, 'words': words, 'value': value},
        {'$inc': {'freq': freq}},
        upsert=True
    )

