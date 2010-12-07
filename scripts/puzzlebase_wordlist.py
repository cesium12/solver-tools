from solvertools.puzzlebase.tables import *
from sqlalchemy import desc
for word in Word.query.order_by(desc(Word.freq)).yield_per(100):
    print "%s,%d" % (word.fulltext.encode('utf-8'), word.freq)
