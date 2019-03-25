# Generation Options

`--bits=(128|160|192|224|256)` Default to 128.  Use the largest prime less than 2**bits for the Shamir secret sharing.  This actually sets the prime number, so this is a write-only parameter.

`--minimum[=#]` Minimum number of share keys to recover secret. **Default** 2. **#** >= 1

`--shares[=#]` Number of share keys to generate. **Default** 4. **#** >= **minimum**

`--prime[=#]` Prime to use for secret sharing. **Default** 2<sup>128</sup>-159.

`--language[=wordlist]`  Default english.  Use given wordlist for dictionary.

`--secret[="some long phrase"]` Set/get secret phrase.

`--key#[="some long phrase"]` Set/get recovery key, ex: --key2="..."

`--randomize` Build random secret and recovery keys.

`--recover` Recover secret and recovery keys from partial information.

`--seed`  Give BIP-39 seed.

`--master` Give BIP-39 HD master key.

`--dump` Create a summary dump of information.

---

+ Previous: [Languages](languages.md "Languages")
+ Next: [Recovering Keys](recoverOverview.md "Recovering Keys")
