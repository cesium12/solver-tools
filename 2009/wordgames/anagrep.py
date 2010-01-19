#! /usr/bin/env python

# anagrep.py
# Copyright 2008 Ben Aisen
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
# 
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above
#       copyright notice, this list of conditions and the following
#       disclaimer in the documentation and/or other materials
#       provided with the distribution.
#     * Neither the name of the Manic Sages nor the names of its
#       contributors may be used to endorse or promote products
#       derived from this software without specific prior written
#       permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

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
