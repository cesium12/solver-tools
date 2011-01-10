from flask import Flask, render_template, request, redirect, url_for, flash
from solvertools.wordlist import ENABLE, WORDNET, WORDNET_DEFS, CROSSWORD, WIKIPEDIA
import socket, urllib
from collections import defaultdict
import logging
#logging.getLogger('sqlalchemy.engine').setLevel(logging.DEBUG)

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

def anagrams(word):
    alph = make_alphagram(word)
    query = elixir.session.query(Word).filter_by(alphagram=alph).order_by(desc(Word.freq)).values(Word.key, Word.fulltext)
    return [text for key, text in query if key != word]

@app.route('/word/<key>')
def word_info(key):
    key = key.replace('_', ' ')
    data = get_word(key)
    if data is None:
        return no_info(key)

    data['anagrams'] = anagrams(word.key)
    data['adjoins'] = []
    data['clues'] = []
    data['bigrams'] = []
    for rel in get_relations(key):
        words = rel['words']
        words.remove(key)
        tagged = [(word, rel.get('interestingness', -10), rel['value']) for word in words]
        if rel == 'can_adjoin':
            data['adjoins'].extend(tagged)
        elif rel == 'clued_by':
            data['clues'].extend(tagged)
        elif rel == 'bigram':
            data['bigrams'].extend(tagged)

    data['crossword_clues'] = crossword_clues(word.key)
    data['wordnet_defs'] = wordnet_defs(word.key)
    return render_template('word_info.html', **data)

def no_info(key):
    return render_template('no_info.html', key=key)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

