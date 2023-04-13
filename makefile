CC = clang
CFLAGS = -std=c99 -Wall -pedantic -fpic
LDFLAGS += -shared -lpython3.7m -L/usr/lib/python3.7/config3.7m-x86_64-linux-gnu

export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:.
# make mol file=test1.c Or whatever test file is used
# mol: libmol.so $(file)
# 	$(CC) $(CFLAGS) -L. -lmol -o mol $(file)

all: libmol.so molecule_wrap.o _molecule.so 

_molecule.so: molecule_wrap.o
	$(CC) $(LDFLAGS)-o -dynamiclib -o _molecule.so molecule_wrap.o libmol.so
	
molecule_wrap.o: molecule_wrap.c
	$(CC) $(CFLAGS)  -c -o molecule_wrap.o molecule_wrap.c -I/usr/include/python3.7m

molecule_wrap.c: molecule.i
	swig3.0 -python molecule.i

libmol.so: mol.o
	$(CC) -shared -o libmol.so mol.o -lm

mol.o: mol.c
	$(CC) $(CFLAGS) -c mol.c

clean:
	rm -f *.o *.so molecule_wrap.c molecule.py

