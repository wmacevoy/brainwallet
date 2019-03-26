CXXFLAGS=-pthread -g -O -std=c++14 -I/usr/local/include -L/usr/local/lib
LDFLAGS=-lntl -lgmp
SHELL=/bin/bash

all : gPrimitivePolysCondensed.py

irreducible : irreducible.cpp
	$(CXX) $(CXXFLAGS) -o $@ $^ $(LDFLAGS)

.PHONY: ntl
ntl :
	F="ntl-11.3.2.tar.gz"; \
	if [ "$$(test ! -f "$$F" && echo "missing" || openssl dgst -sha256 "$$F")" != "$$(cat "$$F.sha256")" ] ; \
	then \
		echo "downloading $$F..."; \
		curl -o $$F https://www.shoup.net/ntl/$$F; \
	fi; \
	if [ "$$(test ! -f "$$F" && echo "missing" || openssl dgst -sha256 "$$F")" == "$$(cat "$$F.sha256")" ] ; \
	then \
		echo "$$F up to date"; \
	else \
		/bin/rm -rf "$$F"; \
	fi

.PHONY: gmp
gmp : 
	F="gmp-6.1.2.tar.xz"; \
	if [ "$$(test ! -f "$$F" && echo "missing" || openssl dgst -sha256 "$$F")" != "$$(cat "$$F.sha256")" ] ; \
	then \
		echo "downloading $$F..."; \
		curl -o $$F https://gmplib.org/download/gmp/$$F; \
	fi; \
	if [ "$$(test ! -f "$$F" && echo "missing" || openssl dgst -sha256 "$$F")" == "$$(cat "$$F.sha256")" ] ; \
	then \
		echo "$$F up to date"; \
	else \
		/bin/rm -rf "$$F"; \
	fi

gPrimitivePolysCondensed.py : Dockerfile Makefile irreducible.cpp ntl gmp
	docker build -t irreducible-ntl .
	docker run --rm -t irreducible-ntl > gPrimitivePolysCondensed.py

.PHONY: install
install : ../brainwallet/gPrimitivePolysCondensed.py

../brainwallet/gPrimitivePolysCondensed.py : gPrimitivePolysCondensed.py
	cp $^ $@
