[![Build Status](https://travis-ci.org/wmacevoy/brainwallet.svg?branch=master)](https://travis-ci.org/wmacevoy/brainwallet)

# Brain Wallet Tools

Python tools for making brainwallet keys

# OS X | Linux | WSL

```bash
./bw <options>
```

# Docker

```bash
docker build -t brainwallet . # once
docker run --rm -t brainwallet:latest bw <options>
```

## Options

`--bits=(128|160|192|224|256)` Default to 128.  Use the largest prime less than 2**bits for the Shamir secret sharing.  This actually sets the prime number, so this is a write-only parameter.

`--minimum[=#]` Default 2. Minimum number of share keys to recover secret.

`--shares[=#]` Default 4. Number of share keys (must be >= minimum) to generate.

`--prime[=#]` Default 2**128-159. Prime to use for secret sharing.

`--language[=wordlist]`  Default english.  Use given wordlist for dictionary.

`--secret[="some long phrase"]` Set/get secret phrase.

`--key#[="some long phrase"]` Set/get recovery key, ex: --key2="..." 

`--randomize` Build random secret and recovery keys.

`--recover` Recover secret and recovery keys from partial information.

`--seed`  Give BIP-39 seed.

`--master` Give BIP-39 HD master key.

`--dump` Create a summary dump of information.

## Ex1: make a 2 out of 5 160 bit secret and recover key set:

```bash
bw --bits=160 --minimum=2 --shares=5 --randomize --dump
```

## Ex2: recover secret and key 2 by providing keys 1 and 3:

```bash
bw --bits=160 --minimum=2 --shares=5 --key1="..." --key3="..." --secret --key2
```

## Ex3: generate HD master key from secret phrase.  DO NOT MAKE UP SECRET - generate it at random.

```bash
bw --secret "..." --master
```

## Ex4: generate HD master from 2 shares:
```bash
bw --bits=160 --minimum=2 --shares=5 --key1="..." --key3="..." --master
```
## Ex5: Get equivalent secrets in French

```bash
bw --bits=160 --minimum=2 --shares=5 --language=english --key1="(english)" --language=french --key1
```

Key recovery phrases (NOT secrets) in different languages can be used interchangeably, and brainwallet will detect the language the phrase is in (or use --language before setting a key or secret for certainty).

```bash
./bw --bits=160 --minimum=2 --shares=5 --key3="abeille garantir impérial écureuil radieux enfouir soleil ethnie empereur fluctuer tamiser aboutir digérer détourer tornade" --key1="ahead copper tonight naive finish rich afford grain swift true virus shrug access gate quantum" --secret
```
