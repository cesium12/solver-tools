from collections import defaultdict
from xml.sax.handler import ContentHandler
from xml.sax import make_parser
from solvertools.lib.tokenize import tokenize_list
from solvertools.util import get_datafile
from solvertools.wordlist import letters_only
import re
import codecs

class WikipediaHandler(ContentHandler):
    def __init__(self, converter):
        self.in_page = False
        self.counts = defaultdict(int)
        self.current_text = ''
        self.converter = converter
    def startElement(self, name, attrs):
        if name == 'text':
            self.in_page = True
    def endElement(self, name):
        if name == 'text':
            self.in_page = False
        self.count_words(self.current_text)
        self.current_text = ''
    def count_words(self, text):
        brackets = 0
        for word in tokenize_list(text.replace('-', ' ')):
            if ':' in word: continue
            if word == '#REDIRECT' or word == '__NOTOC__':
                continue
            if word in "({[<":
                brackets += 1
            elif word in ">]})":
                brackets -= 1
            elif brackets == 0:
                normalword = self.converter(word)
                if normalword:
                    print normalword
                    self.counts[normalword] += 1

    def characters(self, text):
        if self.in_page:
            self.current_text += text

def read_wikipedia(filename, converter):
    parser = make_parser()
    handler = WikipediaHandler(converter)
    parser.setContentHandler(handler)
    parser.parse(filename)
    items = handler.counts.items()
    items.sort(key=lambda x: (-x[1], x[0]))
    return items

def write_wordlist(filename, items, cutoff):
    output = codecs.open(filename, 'w', encoding='utf-8')
    for key, value in items:
        if value >= cutoff:
            print >> output, "%s,%s" % (key,value)
    output.close()

def make_wordlist(data_in, data_out, cutoff):
    items = read_wikipedia(get_datafile(data_in), converter=letters_only)
    write_wordlist(get_datafile(data_out), items, cutoff=cutoff)

#make_wordlist('corpora/wikidumps/lawiki-20101031-pages-articles.xml', 'dict/wikipedia_la.txt', cutoff=4)
make_wordlist('corpora/texts/chaotic.xml', 'dict/chaotic.txt', cutoff=1)

