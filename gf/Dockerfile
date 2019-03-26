FROM debian:stretch
RUN apt-get update && apt-get install -y build-essential make autotools-dev m4
COPY gmp-6.1.2.tar.xz /usr/local
RUN cd /usr/local && tar xf gmp-6.1.2.tar.xz && cd gmp-* && ./configure && make && make check && make install
COPY ntl-11.3.2.tar.gz /usr/local
RUN cd /usr/local && tar xf ntl-11.3.2.tar.gz && cd ntl-*/src && ./configure && make && make check && make install
COPY Makefile irreducible.cpp /usr/local/src/
RUN cd /usr/local/src && make irreducible && cp irreducible /usr/local/bin
CMD /usr/local/bin/irreducible


