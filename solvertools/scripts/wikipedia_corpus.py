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
        for word in tokenize_list(text):
            if ':' in word: continue
            if word == 'REDIRECT' or word == 'NOTOC': continue
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
    items.sort(key=lambda x: -x[1])
    return items

def write_wordlist(filename, items, cutoff):
    output = codecs.open(filename, 'w', encoding='utf-8')
    for key, value in items:
        if value >= cutoff:
            print >> output, "%s,%s" % (key,value)
    output.close()

if __name__ == '__main__':
    items = read_wikipedia(get_datafile('wikidumps/lawiki-20101031-pages-articles.xml'), converter=letters_only)
    write_wordlist(get_datafile('dict/latin.txt'), items, cutoff=4)

