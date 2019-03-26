CXXFLAGS=-pthread -g -O -std=c++14 -I/usr/local/include -L/usr/local/lib
LDFLAGS=-lntl -lgmp
irreducible : irreducible.cpp
	$(CXX) $(CXXFLAGS) -o $@ $^ $(LDFLAGS)
irreducible.py : Dockerfile Makefile irreducible.cpp
	docker build -t irreducible-ntl .
	docker run --rm -t irreducible-ntl > irreducible.py
