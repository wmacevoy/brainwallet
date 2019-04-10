# Generation Options
---
`--bits=(128|160|192|224|256)`
+ Default = 128

Use the largest prime less than 2<sup>bits</sup> for the Shamir secret sharing.
This actually sets the prime number, so this is a write-only parameter.

---

`--minimum[=#]`
Minimum number of share keys to recover secret.

+ Default = 2
+ **minimum** must be >= 1

---

`--shares[=#]`
Number of share keys to generate.

+ Default = 4
+ **shares** must be >= **minimum**

---

`--randomize`
Build random secret and recovery keys.

---

`--dump`
Create a summary dump of information.

> See [Example 1](usage.md#L30-L32) for usage.

---

`--prime[=#]`
Prime to use for secret sharing.

> Do not change this setting unless you know what you are doing.
+ Default  = 2<sup>128</sup>-159.

> Modifying the prime for secrets without proper knowledge could compromise your secret.
Instead, use the `--bits` option to guarantee a prime number, otherwise:

+ **Recommended** any prime >= 2<sup>98</sup>-51
    + See https://primes.utm.edu/lists/2small/100bit.html for probable primes.
    + Make sure that the number is in fact prime for the security of your key.

---

`--key#[="some long phrase"]`
***Possibly being deprecated.***

Set/get recovery key, ex: --key2="..."

> Follow the same caution for recovery phrases as secret phrases, as mentioned above.

---

`--secret[="some long phrase"]`
Set/get secret phrase.

> It is not recommended to "make up" your own phrase.

> Either generate one from third-party software or create one using the Shamir algorithm or a separate algorithm.

> See [Example 2](usage.md#L34-L36) for example usage.
---

`--master`
Give BIP-39 HD master key.

> See [Example 3](usage.md#L38-L40) and [Example 4](usage.md#L42-L44) for example usage.

---

`--language[=wordlist]`
> Uses UTF-8 encoding

Use given wordlist for dictionary.
+ Default = English

> See [Languages](languages.md "Languages") section for supported languages.

> See [Example 5](usage.md#L46-L54) for example usage.

---

`--recover`
***Currently under development (03/25/2019)***

Recover secret and recovery keys from partial information.

---

`--seed`
Give BIP-39 seed.

---

+ Previous: [Languages](languages.md "Languages")
+ Next: [Recovering Keys](recoverOverview.md "Recovering Keys")
