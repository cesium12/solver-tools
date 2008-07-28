#! /usr/bin/env python

from anagram import *

def main():
    dictfile = '/usr/share/dict/words'

    if len(sys.argv) == 1:
        print 'Usage: anagrep [options] length word'
        sys.exit(1)

    (optlist, args) = \
        getopt.getopt(sys.argv[1:], 'd:h',
                      ['dictionary=', 
                       'help'])
    
    for o,a in optlist:
        if o == '-h' or o =='--help':
            usage()
            sys.exit(0)
        elif o == '-d' or o == '--dictionary':
            dictfile = a
        else:
            assert False, 'unhandled option '+o

    if len(args) < 2:
        print 'Usage: anagram [options] length word'
        sys.exit(1)

    length = int(args[0])
    input_word = AnagramWord(' '.join(args[1:]))

    adict = AnagramDict.new_from_file(dictfile, length, length)
    #print 'Dictionary initialized with %d words.' % len(adict.wordlist)

    if length <= input_word.length():
        for w in adict.wordlist:
            if input_word.contains(w): print w
    else:
        for w in adict.wordlist:
            if w.contains(input_word): print w

main()
