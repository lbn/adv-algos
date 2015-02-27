SRC = SuffixTreeQuerier.cpp NaiveSuffixTree.cpp patterns.cpp
OBJ = ${SRC:.cpp=.o}
PROGNAME=patterns

CC=g++
CFLAGS=-std=c++11
all: options ${PROGNAME}

options:
	@echo ${PROGNAME} build options:
	@echo "CFLAGS   = ${CFLAGS}"
	@echo "LDFLAGS  = ${LDFLAGS}"
	@echo "CC       = ${CC}"

.cpp.o:
	@echo CC $<
	@${CC} -c ${CFLAGS} $<


${PROGNAME}: ${OBJ}
	@echo CC -o $@
	@${CC} -o $@ ${OBJ} ${LDFLAGS}

clean:
	@echo cleaning
	@rm -f ${PROGNAME} ${OBJ}

.PHONY: all options clean
