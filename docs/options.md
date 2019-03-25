# Generation Options

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

---

+ Previous: [Languages](languages.md "Languages")
+ Next: [Recovering Keys](recoverOverview.md "Recovering Keys")
