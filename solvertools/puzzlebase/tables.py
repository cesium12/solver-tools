from solvertools.wordlist import alphanumeric_only, Google1M
from solvertools.util import get_db
import elixir, sqlalchemy
from sqlalchemy.orm.exc import NoResultFound
import logging
logger = logging.getLogger(__name__)
elixir.metadata.bind = "sqlite:///"+get_db('puzzlebase.db')
#elixir.metadata.bind.echo = True

def make_alphagram(letters):
    return ''.join(sorted(list(letters)))

class Word(elixir.Entity):
    elixir.using_options(tablename='words')
    key = elixir.Field(elixir.String, primary_key=True)
    fulltext = elixir.Field(elixir.Unicode)
    alphagram = elixir.Field(elixir.String, index=True)
    freq = elixir.Field(elixir.Integer, index=True)
    scrabble = elixir.Field(elixir.Boolean, index=True)
    
    @staticmethod
    def make(text, freq, scrabble=False):
        key = alphanumeric_only(text)
        alphagram = make_alphagram(key)
        obj = Word(key=key, fulltext=text, freq=freq, alphagram=alphagram,
                   scrabble=scrabble)
        elixir.session.add(obj)
        return obj

    @staticmethod
    def get(key):
        try:
            return Word.get_by(key=alphanumeric_only(key))
        except NoResultFound:
            return None

    @staticmethod
    def add_from_wordlist(wordlist, minimum_freq=1000, scrabble=False):
        """
        Add all the words in a wordlist to the database.
        
        The word frequencies come from Google (in the Google1M wordlist).
        `minimum_freq` will increase the frequencies of rarely-Googled words
        that you know are legitimate from another wordlist.

        If `scrabble=True`, it marks this word as being valid for Scrabble
        and similar word games.
        """
        for word in wordlist:
            freq = Google1M.get(word, 0)
            if freq < minimum_freq:
                freq = minimum_freq
            key = alphanumeric_only(word)
            existing = Word.get(key)
            if existing:
                if scrabble:
                    existing.scrabble = True
                    logger.info("Upgrading %s" % word)
                if freq > existing.freq:
                    existing.freq = freq
                    logger.info("Upgrading %s" % word)
            else:
                logger.info("Adding %s" % word)
                Word.make(word, freq, scrabble=scrabble)
        elixir.session.commit()

    def __repr__(self):
        return "%s (%s)" % (self.fulltext, self.freq)

class Relation(elixir.Entity):
    elixir.using_options(tablename='relations')
    id = elixir.Field(elixir.Integer, primary_key=True)
    rel = elixir.Field(elixir.String)
    word1 = elixir.ManyToOne('Word', colname='word1_id')
    word2 = elixir.ManyToOne('Word', colname='word2_id')
    interestingness = elixir.Field(elixir.Float, default=0.0)
    sqlalchemy.UniqueConstraint('rel', 'word1', 'word2')
    
    @staticmethod
    def make(rel, word1, word2):
        if not isinstance(word1, Word):
            word1 = Word.get(word1)
        if not isinstance(word2, Word):
            word2 = Word.get(word2)
        try:
            obj = Relation.get_by(rel=rel, word1=word1, word2=word2)
            return obj
        except NoResultFound:
            obj = Relation(rel=rel, word1=word1, word2=word2)
            elixir.session.add(obj)
            return obj

    @staticmethod
    def make_2way(rel, rev, word1, word2):
        Relation.make(rel, word1, word2)
        Relation.make(rev, word2, word1)

    @staticmethod
    def make_symmetric(rel, word1, word2):
        Relation.make(rel, word1, word2)
        Relation.make(rel, word2, word1)

def commit():
    """
    Commit changes made to the database. External code should remember
    to call this.
    """
    elixir.session.commit()

elixir.setup_all()

