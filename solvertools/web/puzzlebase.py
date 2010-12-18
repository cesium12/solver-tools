from flask import Flask, render_template, request, redirect, url_for, flash
from solvertools.puzzlebase.tables import Word, Relation, make_alphagram, elixir
from solvertools.wordlist import ENABLE, WORDNET, WORDNET_DEFS, CROSSWORD, WIKIPEDIA
import socket, urllib
from sqlalchemy import desc, select
from collections import defaultdict
import logging
#logging.getLogger('sqlalchemy.engine').setLevel(logging.DEBUG)

CROSSWORD.load()
WORDNET.load()

app = Flask(__name__)
app.secret_key='oONHah2hzDJ0CiGyqH3o8mRXijm/JbNg'

@app.route('/')
def start():
    return render_template('start.html')

@app.route('/search')
def search():
    query = request.args.get('q')
    if not query:
        return redirect(url_for('start'))
    return word_info(query)

def crossword_clues(word):
    return list(set(CROSSWORD[word]))

def wordnet_defs(word):
    return list(set(WORDNET_DEFS[word]))

def anagrams(word):
    alph = make_alphagram(word)
    query = elixir.session.query(Word).filter_by(alphagram=alph).order_by(desc(Word.freq)).values(Word.key, Word.fulltext)
    return [text for key, text in query if key != word]

@app.route('/word/<key>')
def word_info(key):
    key = key.replace('_', ' ')
    word = Word.get(key)
    if word is None:
        return no_info(key)

    data = {}
    data['key'] = word.key
    data['fulltext'] = word.fulltext
    data['freq'] = word.freq
    data['relations'] = defaultdict(list)
    data['anagrams'] = anagrams(word.key)
    query = elixir.session.query(Relation).filter_by(word1_id=word.key).join(Relation.word2).order_by(desc(Relation.interestingness), desc(Word.freq)).limit(500).values(Relation.rel, Word.fulltext)
    for rel, word2 in query:
        relname = rel.replace('_', ' ')
        data['relations'][relname].append(word2)
    data['crossword_clues'] = crossword_clues(word.key)
    data['wordnet_defs'] = wordnet_defs(word.key)
    return render_template('word_info.html', **data)

def no_info(key):
    return render_template('no_info.html', key=key)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

