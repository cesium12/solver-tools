# Copyright (c) 2008, Alex Schwendner
# All rights reserved.
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

__author__ = 'alexrs@csail.mit.edu (Alex Schwendner)'


class FreqModel:
    """A simple language model using only single word frequencies.
    
    No context is used, so "HAT" is equally likely as the second word
    of both "PIRATES HAT" and "FREEDOM HAT".
    """

    def __init__(self):
        self.dict_ = {}
        self.total_freq = 0

    def readBNC(self, filename):
        """Reads the file format of the bnc.all.al word list built
        from the British National Corpus.

        Argument filename is the name of the file to open.

        The file should comprise lines of the form
        FREQ1 WORD POS FREQ2
        where
        
        FREQ1 is a measure of frequency (in bnc.all.al, it is the
          number of occurances across all documents)
        WORD is the word
        POS is a CLAWS part of speech tag
        FREQ2 is another measure of frequency (in bnc.all.al, it is
          the number of documents in which the word appears)
        """
        self.dict_ = {}
        self.total_freq = 0
        fin = file(filename, 'r')

        line = fin.readline()
        while line:
            fields = line.split()
            freq = int(fields[0]) + int(fields[3])
            word = fields[1]
            if word.isalpha():
                word = word.upper()
                self.insert(word, freq)
                
            line = fin.readline()

    def all_words(self):
        """Returns a list of all words in the model.
        """
        
        return self.dict_.keys()

    def insert(self, word, freq):
        """Inserts a word with specified additional relative frequency.
        """
        if not word.isalpha(): return
        word = word.upper()
        if word in self.dict_:
            self.dict_[word] += freq
        else:
            self.dict_[word] = freq
        self.total_freq += freq

    def prob(self, word, context=[]):
        """Returns the model's estimated probability of a word given
        the preceding words.

        Argument word is a string containing the next word.

        Argument context is a list of strings containing some number
        of preceding words. The list is not reversed, so context[-1]
        is the immediately preceding word.

        The returned probability will be a real number in the interval
        [0,1].
        """
        
        f = self.dict_.get(word.upper(), 0)
        return f / float(self.total_freq)

    def trim_context(self, context):
        """Takes a list of words and returns the suffix of that list
        that might potentially effect the probabilities for the next
        word."""
        return []
