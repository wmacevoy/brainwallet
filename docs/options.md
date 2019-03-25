# Generation Options

`--bits=(128|160|192|224|256)`

**Default** = 128

Use the largest prime less than 2<sup>bits</sup> for the Shamir secret sharing.
This actually sets the prime number, so this is a write-only parameter.

`--minimum[=#]` Minimum number of share keys to recover secret.

**Default** = 2
**minimum** >= 1

`--shares[=#]` Number of share keys to generate.

**Default** = 4
**shares** >= **minimum**

`--prime[=#]` Prime to use for secret sharing.

**Default**  = 2<sup>128</sup>-159.

***Do not change this setting unless you know what you are doing.***
Modifying the prime for secrets without proper knowledge could comprimise your secret.

Instead, use the `--bits` option to guarentee a prime number

**Recommended** any prime >= 2<sup>98</sup>-51
+ Use resources such as https://primes.utm.edu/lists/2small/100bit.html for probable primes.
+ Make sure that the number is in fact prime for the security of your key.

`--language[=wordlist]` Use given wordlist for dictionary.

**Default** = English
*See [Languages](languages.md "Languages") section for supported languages.*

`--secret[="some long phrase"]` Set/get secret phrase.

***It is not recommended to "make up" your own phrase.***

Either generate one from third-party software or create one using the Shamir algorithm or a separate algorithm.

`--key#[="some long phrase"]` Set/get recovery key, ex: --key2="..."

***Possibly being deprecated.***

***Follow the same caution for recovery phrases as secret phrases***, as mentioned above.

`--randomize` Build random secret and recovery keys.

`--recover` Recover secret and recovery keys from partial information.

***Currently under development (03/25/2019)***

`--seed`  Give BIP-39 seed.

`--master` Give BIP-39 HD master key.

`--dump` Create a summary dump of information.

---

+ Previous: [Languages](languages.md "Languages")
+ Next: [Recovering Keys](recoverOverview.md "Recovering Keys")
