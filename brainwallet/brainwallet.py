#!/usr/bin/env python

from shamir import Shamir
from phrases import Phrases
from check import Check
from rng import RNG

class BrainWallet:
    DEFAULT_MINIMUM = 2
    DEFAULT_SHARES  = 4
    DEFAULT_PRIME = 2**256 - 2**32 - 2**9 - 2**8 - 2**7 - 2**6 - 2**4 - 1
    DEFAULT_LANGUAGE = "english"

    def __init__(self, minimum=DEFAULT_MINIMUM, shares=DEFAULT_SHARES, prime=DEFAULT_PRIME, language=DEFAULT_LANGUAGE):
        self._shamir = Shamir(minimum,shares,prime)
        self._phrases = Phrases.forLanguage(language)

    def getMinimum(self):
        return self._shamir.getMinimum()
    def getShares(self):
        return self._shamir.getShares()
    def getPrime(self):
        return self._shamir.getPrime()
    def getLanguage(self):
        return self._phrases.language

    def number(self,phrase):
        if Check.isInt(phrase): return phrase
        return self._phrases.toNumber(phrase)

    def phrase(self,number):
        if Check.isString(number): return number
        return self._phrases.toPhrase(number)

    def getSecret(self):
        return self.phrase(self._shamir.getSecret())
    def setSecret(self,value):
            self._shamir.setSecret(self.number(value))
    def getKey(self,index):
        index = Check.toInt(index,"index",1,self._shamir.getShares())
        return self.phrase(self._shamir.getKey(index))

    def setKey(self,index,value):
        index = Check.toInt(index,"index",1,self._shamir.getShares())        
        self._shamir.setKey(self.number(value))

    def randomize(self):
        self._shamir.setRandomSecret()
        self._shamir.makeKeys()

    def recover(self):
        self._shamir.recoverKeys()

    def dump(self):
        print ("secret: " + self.getSecret())
        for i in range(1,self.getShares()+1):
            print ("key#" + str(i) + ": " + self.getKey(i))
        print ("Secret can be recovered with any " + str(self.getMinimum()) + " of the " + str(self.getShares()) + " keys.")
        print ("Remember the key number (#1-#" + str(self.getShares()) + ") and phrase.")

def main():
    brainWallet=BrainWallet()
    brainWallet.randomize()
    brainWallet.dump()

if __name__ == "__main__":
    main()

