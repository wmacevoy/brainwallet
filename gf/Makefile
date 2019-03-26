CXXFLAGS=-pthread -g -O -std=c++14 -I/usr/local/include -L/usr/local/lib
LDFLAGS=-lntl -lgmp
SHELL=/bin/bash
irreducible : irreducible.cpp
	$(CXX) $(CXXFLAGS) -o $@ $^ $(LDFLAGS)

.PHONY: ntl-11.3.2.tar.gz
ntl-11.3.2.tar.gz :
	F="$@"; \
	if [ "$$(test ! -f "$$F" && echo "missing" || openssl dgst -sha256 "$$F")" != "$$(cat "$$F.sha256")" ] ; \
	then \
		echo "downloading $$F..."; \
		curl -o $$F https://www.shoup.net/ntl/$$F; \
	fi; \
	if [ "$$(test ! -f "$$F" && echo "missing" || openssl dgst -sha256 "$$F")" == "$$(cat "$$F.sha256")" ] ; \
	then \
		echo "$$F up to date"; \
		touch "$$F"; \
	else \
		/bin/rm -rf "$$F"; \
	fi

.PHONY: gmp-6.1.2.tar.xz
gmp-6.1.2.tar.xz :
	F="$@"; \
	if [ "$$(test ! -f "$$F" && echo "missing" || openssl dgst -sha256 "$$F")" != "$$(cat "$$F.sha256")" ] ; \
	then \
		echo "downloading $$F..."; \
		curl -o $$F https://gmplib.org/download/gmp/$$F; \
	fi; \
	if [ "$$(test ! -f "$$F" && echo "missing" || openssl dgst -sha256 "$$F")" == "$$(cat "$$F.sha256")" ] ; \
	then \
		echo "$$F up to date"; \
		touch "$$F"; \
	else \
		/bin/rm -rf "$$F"; \
	fi

irreducible.py : Dockerfile Makefile irreducible.cpp ntl-11.3.2.tar.gz gmp-6.1.2.tar.xz
	docker build -t irreducible-ntl .
	docker run --rm -t irreducible-ntl > irreducible.py
