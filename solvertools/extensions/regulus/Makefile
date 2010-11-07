UNAME := $(shell uname)

CPPFLAGS = -Wall -O3 -fpic -ffast-math -pipe `python-config --cflags`
ifeq ($(UNAME), Linux)
objs = amtrie.o automaton.o check.o dict.o dyntrie.o
endif
ifeq ($(UNAME), Darwin)
objs = amtrie.o automaton.o check.o dict.o dyntrie.o /System/Library/Frameworks/Python.framework/Versions/2.6/Python 
endif
_regulus.so: $(objs) regulus_wrap.o
	g++ -shared -dynamiclib $(CPPFLAGS) $(objs) regulus_wrap.o -o _regulus.so

regulus_wrap.cpp:
	swig -c++ -python -o regulus_wrap.cpp regulus.i

regex_test: $(objs) regex_test.o
	g++  $(CPPFLAGS)  regex_test.o $(objs) -o regex_test

.PHONY : clean
clean:
	rm -f *.o _regulus.so regulus_wrap.cpp

SOURCES = $(filter-out regulus_wrap.cpp, $(wildcard *.cpp *.h))

Makefile.depends: $(SOURCES)
	g++ $(SOURCES) -MM > Makefile.depends

-include Makefile.depends
