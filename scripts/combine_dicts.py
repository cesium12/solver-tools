from solvertools.wordlist import *
from solvertools.util import *
import codecs

# Include words that do not appear in any wordlist but might very well appear
# in a puzzle.
extras = ['XKCD', 'ZYZZLVARIA', 'KONUNDRUM', 'HOCKFIELD', 'IHTFP']

out = codecs.open(get_dictfile('sages_combined.txt'), 'w', encoding='utf-8')
used_words = set()
for word, freq in Google200K.iteritems():
    print word, freq
    used_words.add(word)
    out.write(u"%s,%d\n" % (word, freq))
del Google200K

for word, freq in PHRASES.iteritems():
    print word, freq
    used_words.add(word)
    out.write(u"%s,%d\n" % (word, freq))
del PHRASES

for word in ENABLE:
    if word not in used_words:
        print word
        used_words.add(word)
        out.write(u"%s,10000\n" % word)
del ENABLE

for word in extras:
    if word not in used_words:
        print word
        used_words.add(word)
        out.write(u"%s,10000\n" % word)

for word in PHONETIC:
    word = alphanumeric_and_spaces(word)
    if word not in used_words:
        print word
        used_words.add(word)
        out.write(u"%s,10000\n" % word)

for word in WORDNET:
    word = alphanumeric_and_spaces(word)
    if word not in used_words:
        print word
        used_words.add(word)
        out.write("%s,10000\n" % word)

for word in NPL:
    word = alphanumeric_and_spaces(word)
    if word not in used_words:
        print word
        used_words.add(word)
        out.write(u"%s,1000\n" % word)
out.close()

