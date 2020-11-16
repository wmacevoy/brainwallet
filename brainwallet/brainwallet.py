#!/usr/bin/env python

import binascii
import hashlib
import hmac
import math
import sys
import re

from shamir import Shamir
from phrases import Phrases
from check import Check
from millerrabin import MillerRabin


class BrainWallet:
    DEFAULT_MINIMUM = None
    DEFAULT_SHARES  = None
    DEFAULT_ORDERED = True
    DEFAULT_PRIME = 2**132 - 347
    DEFAULT_LANGUAGE = "english"
    PBKDF2_ROUNDS = 2048

    def __init__(self):
        self._minimum = None
        self._shares = None
        self._prime = None
        self._language = None
        self._ordered = None
        self._keys = dict()
        self._millerRabin = MillerRabin()

    def getMinimum(self):
        return self._minimum if self._minimum is not None \
            else self.DEFAULT_MINIMUM

    def setMinimum(self, value):
        self._minimum = Check.toInt(value, "minimum", 1)

    def getShares(self):
        return self._shares

    def setShares(self,value):
        self._shares = Check.toInt(value,"shares",1)

    def getOrdered(self):
        return self._ordered if self._ordered != None else self.DEFAULT_ORDERED

    def setOrdered(self,value):
        self._ordered = Check.toBoolean(value)
        
    def setShares(self, value):
        self._shares = Check.toInt(value, "shares", 1)

    def getPrime(self):
        return self._prime if self._prime != None else self.DEFAULT_PRIME

    def setBits(self, bits):
        bits = Check.toInt(bits, "bits", 96, 256)
        self.setPrime(self._millerRabin.prevPrime(2**bits))

    def getBits(self):
        prime = self.getPrime()
        bits = int(math.ceil(math.log(prime, 2)))
        # correct for floating point errors
        while 2**(bits-1) >= prime:
            bits = bits - 1
        while 2**bits < prime:
            bits = bits + 1
        if (self._millerRabin.prevPrime(2**bits) != prime):
            bits = None
        return bits

    def setPrime(self, prime):
        self._prime = Check.toPrime(prime)

    def getLanguage(self):
        return self._language if self._language is not None \
            else self.DEFAULT_LANGUAGE

    def setLanguage(self, language):
        language = Check.toString(language)
        if not (language in Phrases.getLanguages()):
            raise ValueError("language missing")
        self._language = language

    def _getShamir(self):
        shamir = Shamir(self.getMinimum(), self.getPrime())
        for i in self._keys:
            shamir.setKey(i, self._keys[i])
        return shamir

    def _getPhrases(self):
        return Phrases.forLanguage(self.getLanguage())

    def number(self, phrase, ordered = None):
        phrase = Check.toString(phrase)
        phrases = self._getPhrases()
        if ordered == None:
            ordered = self.getOrdered()
        if not phrases.isPhrase(phrase):
            detects = Phrases.detectLanguages(phrase)
            phrases = Phrases.forLanguage(detects[0]) if len(detects) == 1 else None
        if phrases == None:
            raise ValueError("unknown phrase language")
        return phrases.toNumber(phrase,ordered)

    def phrase(self, number, ordered = None):
        number = Check.toInt(number)
        if ordered == None:
            ordered = self.getOrdered()
        return self._getPhrases().toPhrase(number, ordered)

    def getSecret(self):
        return self.getKey(0)

    def setSecret(self, phrase, ordered = None):
        self.setKey(0, phrase, ordered)

    def getKey(self, index, ordered = None):
        name = "index" if index > 0 else "secret"
        index = Check.toInt(index, name, 0)
        if index not in self._keys:
            self._keys[index] = self._getShamir().getKey(index)
        return self.phrase(self._keys[index],ordered)

    def setKey(self, index, phrase, ordered = None):
        name = "index" if index > 0 else "secret"
        index = Check.toInt(index, name)
        self._keys[index] = self.number(phrase, ordered)

    def randomize(self):
        self.randomizeSecret()
        self.randomizeKeys()

    def randomizeSecret(self):
        shamir = self._getShamir()
        shamir.randomizeSecret()
        self._keys = dict()
        self._keys[0] = shamir.getSecret()

    def randomizeKeys(self):
        secret = self._keys[0] if 0 in self._keys else None
        shares = self.getShares()
        minimum = self.getMinimum()
        if secret == None:
            raise ValueError("secret must be set")
        if minimum is None:
            raise ValueError("minimum must be set")
        if shares is None:
            raise ValueError("shares must be set")
        if shares < minimum:
            raise ValueError("shares must be >= minimum")
        shamir = self._getShamir()
        shamir.randomizeKeys(shares)
        self._keys = dict()
        self._keys[0] = secret
        for index in range(1, shares + 1):
            self._keys[index] = shamir.getKey(index)

    def getSeed(self, salt=""):
        password = self.getSecret().encode("utf-8")
        salt = (u"mnemonic" + salt).encode("utf-8")
        iterations = self.PBKDF2_ROUNDS
        stretched = hashlib.pbkdf2_hmac('sha512', password, salt, iterations)
        return stretched[0:64]

    # Refactored code segments from <https://github.com/keis/base58>
    B58_ALPHABET = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"

    @classmethod
    def b58encode(cls, data):
        p = 1
        acc = 0
        for c in reversed(data):
            if not Check.PYTHON3:
                c = ord(c)
            acc += p * c
            p = p << 8

        string = ""
        while True:
            acc, idx = divmod(acc, 58)
            string = cls.B58_ALPHABET[idx: idx + 1] + string
            if acc == 0: break
        return string

    @classmethod
    def getHDMasterKey(cls, seed):
        if len(seed) != 64:
            raise ValueError("Provided seed should have length of 64")

        seed = hmac.new(b"Bitcoin seed", seed,
                        digestmod=hashlib.sha512).digest()

        # Serialization format can be found at:
        # https://github.com/bitcoin/bips/blob/master/bip-0032.mediawiki#Serialization_format
        xprv = b"\x04\x88\xad\xe4"  # Version for private mainnet
        xprv += b"\x00" * 9  # Depth, parent fingerprint, and child number
        xprv += seed[32:]  # Chain code
        xprv += b"\x00" + seed[:32]  # Master key

        # Double hash using SHA256
        hashed_xprv = hashlib.sha256(xprv).digest()
        hashed_xprv = hashlib.sha256(hashed_xprv).digest()

        # Append 4 bytes of checksum
        xprv += hashed_xprv[:4]

        # Return base58
        return cls.b58encode(xprv)

    def dump(self):
        prime = self.getPrime()
        bits = self.getBits()
        shares = self.getShares()
        minimum = self.getMinimum()
        language = self.getLanguage()

        if self.getOrdered() != self.DEFAULT_ORDERED:
            print ("--ordered=" +(str(self.getOrdered()).lower()))

        ordering = "unordered-" if not self.getOrdered() else ""
            
        print ("--language=%s" % language)
        if bits is not None:
            print ("--bits=%d" % bits)
        else:
            print ("--prime=%d" % prime)
        if minimum != None:
            print ("--minimum=%d" % minimum)
        if shares != None:
            print ("--shares=%d" % shares)
        if 0 in self._keys:
            print ("--%ssecret=\"%s\"" % (unordered,self._encode2(self.getSecret())))
        for i in range(1, self.getShares() + 1):
            if i in self._keys:
                print ("--%skey%d=\"%s\"" % (unordered,i,self._encode2(self.getKey(i))))
        print ("Secret can be recovered with any %d of the %d keys" %
               (minimum, shares))
        print ("Remember the key id (1-%d) and corresponding phrase." % shares)

    @classmethod
    def encode2(cls,msg):
        return msg if Check.PYTHON3 else msg.encode("utf-8")

    def cli(self, args):
        for i in range(len(args)):
            arg = args[i]

            cmd = "--ordered"
            if arg == cmd:
                print(str(self.getOrdered()).lower())
                continue
            if arg.startswith(cmd + "="):
                self.setOrdered(arg[len(cmd) + 1:].lower() == "true")
                continue

            cmd = "--language"
            if arg == cmd:
                print(self.getLanguage())
                continue
            if arg.startswith(cmd + "="):
                self.setLanguage(arg[len(cmd) + 1:])
                continue

            cmd = "--minimum"
            if arg == cmd:
                print(self.getMinimum())
                continue
            if arg.startswith(cmd + "="):
                self.setMinimum(arg[len(cmd) + 1:])
                continue

            cmd = "--shares"
            if arg == cmd:
                print(self.getShares())
                continue
            if arg.startswith(cmd + "="):
                self.setShares(arg[len(cmd) + 1:])
                continue

            cmd = "--prime"
            if arg == cmd:
                print(self.getPrime())
                continue
            if arg.startswith(cmd + "="):
                self.setPrime(arg[len(cmd) + 1:])
                continue

            cmd = "--bits"
            if arg == cmd:
                print(self.getBits())
                continue
            if arg.startswith(cmd + "="):
                self.setBits(arg[len(cmd) + 1:])
                continue

            match = re.search('^--(ordered-|unordered-|)(secret|key([0-9]+))((=)(.*))?$', arg)
            if match:
                ordered = None
                if match.group(1) == "ordered-": ordered = True
                if match.group(1) == "unordered-": ordered = False
                index = int(match.group(3)) if match.group(2) != "secret" else 0
                if match.group(5) == "=":
                    self.setKey(index,match.group(6),ordered)
                    continue
                else:
                    print(self.encode2(self.getKey(index,ordered)))
                    continue
            cmd = "--randomize"
            if arg == cmd:
                self.randomize()
                continue
            cmd = "--randomizeSecret"
            if arg == cmd:
                self.randomizeSecret()
                continue
            cmd = "--randomizeKeys"
            if arg == cmd:
                self.randomizeKeys()
                continue
            cmd = "--dump"
            if arg == cmd:
                self.dump()
                continue
            cmd = "--seed"
            if arg == cmd:
                print (binascii.hexlify(self.getSeed()))
                continue
            cmd = "--master"
            if arg == cmd:
                seed = self.getSeed()
                key = self.getHDMasterKey(seed)
                print (key)
                continue
            raise ValueError("unknown command " + arg)

def main():
    brainWallet = BrainWallet()
    brainWallet.cli(sys.argv[1:])


if __name__ == "__main__":
    main()
