FROM python:2.7-alpine
RUN apk add bash
COPY bw /usr/local/brainwallet/
COPY brainwallet /usr/local/brainwallet/brainwallet/
RUN chmod +x /usr/local/brainwallet/bw && \
    ln -s /usr/local/brainwallet/bw /usr/local/bin 
ENV HOME /home
WORKDIR /home

