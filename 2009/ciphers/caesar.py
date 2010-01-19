#! /usr/bin/env python

# caesar.py
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


import string, sys
from operator import isNumberType

class CaesarCipher:
    def __init__(self,
                 lower_alph = string.ascii_lowercase,
                 upper_alph = string.ascii_uppercase):
        self.l_alph = lower_alph
        self.u_alph = upper_alph


    def encipher(self,key,plaintext):
        return plaintext.translate(self.transtable(key,inv = False))

    def decipher(self,key,ciphertext):
        return ciphertext.translate(self.transtable(key,inv = True))

    def transtable(self,key,inv = False):
        if isNumberType(key):
            k = key%26
        elif key in self.l_alph:
            k = self.l_alph.index(key)
        elif key in self.u_alph:
            k = self.u_alph.index(key)
        else:
            raise ValueError, 'Bad key value "%s"' % key

        from_alph = self.l_alph + self.u_alph
        to_alph = self.l_alph[k:] + self.l_alph[:k] + self.u_alph[k:] + \
            self.u_alph[:k]
        if inv:
            return string.maketrans(to_alph,from_alph)
        else:
            return string.maketrans(from_alph,to_alph)

if __name__ == '__main__':
    # ROT13 demo.
    c = CaesarCipher()
    try:
        while True:
            print c.encipher(13,raw_input())
    except EOFError:
        pass
