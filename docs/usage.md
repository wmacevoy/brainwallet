# Usage

The Brainwallet software is compatible with OS X and Linux operating systems and WSL for Windows, using Python 2 or 3.

`./your/path/to/bw <options>`

## Docker

For those wishing to use Docker, ensure that Docker is running, and then follow these steps:

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

<a name="one"></a>

1. Make a 2 out of 5 160 bit secret and recover key set:

    `bw --bits=160 --minimum=2 --shares=5 --randomize --dump`

    ##### Output:

    ```
    2
    4
    --language=english
    --bits=160
    --prime=1461501637330902918203684832716283019655932542929
    --minimum=2
    --shares=4
    --secret="always traffic bacon first crystal pistol sadness state visa misery degree nature fork glow mango"
    --key1="aim runway obscure memory loan noise pause build about task gain toilet seven system slam"
    --key2="adapt neither butter salmon speak mail luggage grit arrange common loop crowd come field auction"
    --key3="absorb hello play velvet burden isolate habit question blossom learn pottery lucky nuclear solve fan"
    --key4="alley dose coin cereal hobby group entire wear cat song social steel absent elevator move"
    Secret can be recovered with any 2 of the 4 keys
    Remember the key id (1-4) and corresponding phrase.
    ```

<a name="two"></a>

2. Recover secret and key 2 by providing keys 1 and 3:

    `bw --bits=160 --minimum=2 --shares=5 --key1="..." --key3="..." --secret --key2`

    ##### Output (using above keys):
    ```
    always traffic bacon first crystal pistol sadness state visa misery degree nature fork glow mango
    adapt neither butter salmon speak mail luggage grit arrange common loop crowd come field auction
    ```

3. Generate HD master key from secret phrase.  ***Do not "make up" secret*** - generate it at random.

    `bw --secret "..." --master`

4. Generate HD master from 2 shares:

    `bw --bits=160 --minimum=2 --shares=5 --key1="..." --key3="..." --master`

5. Get equivalent secrets in French

    `bw --bits=160 --minimum=2 --shares=5 --language=english --key1="(english)" --language=french --key1`

> Key recovery phrases (NOT secrets) in different languages can be used interchangeably, and brainwallet will detect the language the phrase is in (or use --language before setting a key or secret for certainty).

```
bw --bits=160 --minimum=2 --shares=5 --key3="abeille garantir impérial écureuil radieux enfouir soleil ethnie empereur fluctuer tamiser aboutir digérer détourer tornade" --key1="ahead copper tonight naive finish rich afford grain swift true virus shrug access gate quantum" --secret
```

---

+ Previous: [Home Page](README.md "Home Page")
+ Next: [Creating Keys](createOverview.md "Creating Keys")
