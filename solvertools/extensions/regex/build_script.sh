#!/bin/sh
# Someone make this into a Makefile.
swig -c++ -python -module regex -o regex_wrap.cpp regex.i
g++ -c -fpic -Wall -O3 -ffast-math -pipe -I/System/Library/Frameworks/Python.framework/Versions/2.6/include/python2.6/ *.cpp
g++ -shared *.o -o _regex.so
