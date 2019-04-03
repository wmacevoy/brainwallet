# Usage

The Brainwallet software is compatible with OS X and Linux operating systems and \
WSL for Windows, using Python 2 or 3.

`./your/path/to/bw <options>`

## Docker

For those wishing to use Docker to run the Brainwallet software, follow these steps:

### Build:

Navigate to the brainwallet directory containing Dockerfile and in the command-line interface:

**Run Once**
```
docker build -t brainwallet
```

### Run:

```
docker run --rm -t brainwallet:latest bw <options>
```

## Example Usage

> See the Options section of Creating Keys for more details.

+ Make a 2 out of 5 160 bit secret and recover key set:

`bash
bw --bits=160 --minimum=2 --shares=5 --randomize --dump
`

+ Recover secret and key 2 by providing keys 1 and 3:

```bash
bw --bits=160 --minimum=2 --shares=5 --key1="..." --key3="..." --secret --key2
```

+ Generate HD master key from secret phrase.  DO NOT MAKE UP SECRET - generate it at random.

```bash
bw --secret "..." --master
```

+ Generate HD master from 2 shares:
```bash
bw --bits=160 --minimum=2 --shares=5 --key1="..." --key3="..." --master
```
+ Get equivalent secrets in French

```bash
bw --bits=160 --minimum=2 --shares=5 --language=english --key1="(english)" --language=french --key1
```

> Key recovery phrases (NOT secrets) in different languages can be used interchangeably, and brainwallet will detect the language the phrase is in (or use --language before setting a key or secret for certainty).

```bash
./bw --bits=160 --minimum=2 --shares=5 --key3="abeille garantir impérial écureuil radieux enfouir soleil ethnie empereur fluctuer tamiser aboutir digérer détourer tornade" --key1="ahead copper tonight naive finish rich afford grain swift true virus shrug access gate quantum" --secret
```

---

+ Previous: [Home Page](README.md "Home Page")
+ Next: [Creating Keys](createOverview.md "Creating Keys")
