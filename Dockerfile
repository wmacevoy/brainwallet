FROM debian:jessie-slim

RUN \
  DEBIAN_FRONTEND=noninteractive \
    apt-get update && apt-get install --assume-yes --no-install-recommends \
      build-essential \
      curl \
      git \
      nasm \
      openssl \
      python \
      python-pip \
      ssss \
      unzip \
      vim-common \
      wget \
      zip

ENV HOME /home
WORKDIR /home

RUN  COMMIT=493e324df9b70e3bb195984fe6e86e01a477c777; curl -L https://github.com/trezor/python-mnemonic/archive/$COMMIT.zip > /usr/local/python-mnemonic.zip && cd /usr/local && unzip python-mnemonic.zip && mv python-mnemonic-$COMMIT python-mnemonic && cd python-mnemonic && pip install -r requirements.txt && python setup.py install
COPY mnemonic /usr/local/bin/
RUN  chmod +x /usr/local/bin/mnemonic


