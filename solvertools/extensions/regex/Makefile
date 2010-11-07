UNAME := $(shell uname)

ifeq ($(UNAME), Linux)
PYTHONLIB=/usr/include/python2.6/
endif
ifeq ($(UNAME), Darwin)
PYTHONLIB=/System/Library/Frameworks/Python.framework/Versions/2.6/include/python2.6/
endif


CPPFLAGS = -Wall -O3 -fpic -ffast-math -march=native -pipe -I$(PYTHONLIB)

objs = amtrie.o automaton.o check.o dict.o dyntrie.o

_regex.so: $(objs) regex.o
	g++ -shared -dynamiclib -u _PyMac_Error $(CPPFLAGS) $(objs) regex.o -o _regex.so

regex.cpp:
	swig -c++ -python -o regex.cpp regex.i

regex_test: $(objs) regex_test.o
	g++  $(CPPFLAGS)  regex_test.o $(objs) -o regex_test

.PHONY : clean
clean:
	rm -f *.o _regex.so regex_wrap.cpp

Makefile.depends: *.cpp *.h
	rm -f regex.cpp
	g++ *.cpp -MM > Makefile.depends

include Makefile.depends
