from solvertools.wordlist import COMBINED_WORDY, alphanumeric_only
from solvertools.util import get_db
from elixir import metadata, session, Entity, Field, String, Integer, Float,\
                   ManyToOne, using_options
import elixir
from sqlalchemy import UniqueConstraint
from sqlalchemy.orm.exc import NoResultFound
import logging
logger = logging.getLogger(__name__)
metadata.bind = "sqlite:///"+get_db('puzzlebase.db')
#metadata.bind.echo = True

def make_alphagram(letters):
    return ''.join(sorted(list(letters)))

class Word(Entity):
    using_options(tablename='words')
    key = Field(String, primary_key=True)
    fulltext = Field(String)
    alphagram = Field(String, index=True)
    freq = Field(Integer, index=True)
    
    @staticmethod
    def make(text, freq):
        key = alphanumeric_only(text)
        alphagram = make_alphagram(key)
        obj = Word(key=key, fulltext=text, freq=freq, alphagram=alphagram)
        session.add(obj)
        return obj

    @staticmethod
    def get(key):
        try:
            return Word.get_by(key=alphanumeric_only(key))
        except NoResultFound:
            return None

    @staticmethod
    def build_table():
        for word in COMBINED_WORDY:
            freq = COMBINED_WORDY[word]
            key = alphanumeric_only(word)
            if not Word.get(key):
                logger.info("Adding %s" % word)
                Word.make(word, freq)
        session.commit()

    def __repr__(self):
        return "%s (%s)" % (self.fulltext, self.freq)

class Relation(Entity):
    using_options(tablename='relations')
    id = Field(Integer, primary_key=True)
    rel = Field(String)
    word1 = ManyToOne('Word', colname='word1_id')
    word2 = ManyToOne('Word', colname='word2_id')
    interestingness = Field(Float, default=0.0)
    UniqueConstraint('rel', 'word1', 'word2')
    
    @staticmethod
    def make(rel, word1, word2):
        if not isinstance(word1, Word):
            word1 = Word.get(word1)
        if not isinstance(word2, Word):
            word2 = Word.get(word2)
        obj = Relation(rel=rel, word1=word1, word2=word2)
        session.add(obj)
        return obj

    @staticmethod
    def make_2way(rel, rev, word1, word2):
        Relation.make(rel, word1, word2)
        Relation.make(rev, word2, word1)

    @staticmethod
    def make_symmetric(rel, word1, word2):
        Relation.make(rel, word1, word2)
        Relation.make(rev, word2, word1)

elixir.setup_all()

