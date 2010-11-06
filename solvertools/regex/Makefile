CPPFLAGS = -Wall -O3 -ffast-math -march=native -pipe

objs = amtrie.o automaton.o check.o dyntrie.o langmodel.o lognum.o regex.o

regex_test: $(objs) regex_test.o
	g++  $(CPPFLAGS)  regex_test.o $(objs) -o regex_test

clean:
	rm *.o



amtrie.o: amtrie.cpp amtrie.h dyntrie.h
automaton.o: automaton.cpp automaton.h lognum.h
check.o: check.cpp check.h
dyntrie.o: dyntrie.cpp check.h dyntrie.h
langmodel.o: langmodel.cpp check.h dyntrie.h langmodel.h amtrie.h
lognum.o: lognum.cpp lognum.h
