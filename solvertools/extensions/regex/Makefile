UNAME := $(shell uname)

BOOST_PREFIX = /Users/rspeer/src/boost_1_44_0/
CPPFLAGS = -Wall -O3 -fpic -ffast-math -pipe `python-config --cflags` -I$(BOOST_PREFIX)
ifeq ($(UNAME), Linux)
objs = amtrie.o automaton.o check.o dict.o dyntrie.o
endif
ifeq ($(UNAME), Darwin)
objs = amtrie.o automaton.o check.o dict.o dyntrie.o /System/Library/Frameworks/Python.framework/Versions/2.6/Python 
endif
_regex.so: $(objs) regex.o
	g++ -shared -dynamiclib $(CPPFLAGS) $(objs) regex.o -o _regex.so

regex.cpp:
	swig -c++ -python -o regex.cpp regex.i

regex_test: $(objs) regex_test.o
	g++  $(CPPFLAGS)  regex_test.o $(objs) -o regex_test

.PHONY : clean
clean:
	rm -f *.o _regex.so regex_wrap.cpp

Makefile.depends: *.cpp *.h
	g++ *.cpp -MM > Makefile.depends

include Makefile.depends
