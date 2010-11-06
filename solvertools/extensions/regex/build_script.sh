#!/bin/sh
# Someone make this into a Makefile.
swig -c++ -python -o regex_wrap.cpp regex.i
g++ -c -fpic -Wall -O3 -ffast-math -pipe -I/usr/include/python2.6/ amtrie.cpp dyntrie.cpp langmodel.cpp lognum.cpp regex.cpp check.cpp automaton.cpp regex_wrap.cpp
g++ -shared -dynamiclib -u _PyMac_Error /usr/include/python2.6/Python.h automaton.o amtrie.o check.o dyntrie.o langmodel.o lognum.o regex.o regex_wrap.o -o _regex.so
