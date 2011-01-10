from solvertools.puzzlebase.mongo import DB, get_word, get_relations, get_anagrams
from solvertools.puzzlebase.clue import match_clue
from flask import Flask, render_template, request, redirect, url_for, flash
from solvertools.wordlist import alphanumeric_only, CROSSWORD, WORDNET_DEFS
import socket, urllib
from collections import defaultdict
import logging
from solvertools.config import DB_USERNAME, DB_PASSWORD

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
    if ' ' not in query:
        return word_info(query)
    else:
        return solve_clue(query)

@app.route('/clue/<clue>')
def solve_clue(clue):
    DB.authenticate(DB_USERNAME, DB_PASSWORD)
    answers = match_clue(clue)
    if not answers:
        return no_info(key)
    return render_template('clue.html', clue=clue, answers=answers)

@app.route('/word/<key>')
def word_info(key):
    DB.authenticate(DB_USERNAME, DB_PASSWORD)
    key = alphanumeric_only(key.replace('_', ' '))
    query = get_word(key)
    if query is None:
        return no_info(key)
    data = {}
    data['freq'] = query['freq']
    data['text'] = query['text']
    data['key'] = query['key']
    data['anagrams'] = [word for word, freq in get_anagrams(key)]
    data['adjoins'] = []
    data['clues'] = []
    data['bigrams'] = []
    for rel in get_relations(key)[:1000]:
        words = rel['words']
        words.remove(key)
        tagged = [(word, rel.get('interestingness', -10), rel['value']) for word in words]
        if rel['rel'] == 'can_adjoin':
            data['adjoins'].extend(tagged)
        elif rel['rel'] == 'clued_by':
            data['clues'].extend(tagged)
        elif rel['rel'] == 'bigram':
            data['bigrams'].extend(tagged)
    data['crossword_clues'] = CROSSWORD[key]
    data['wordnet_defs'] = WORDNET_DEFS[key]
    return render_template('word_info.html', **data)

def no_info(key):
    return render_template('no_info.html', key=key)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

