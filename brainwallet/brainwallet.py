#!/usr/bin/env python

import sys
import binascii
from shamir import Shamir
from phrases import Phrases
from check import Check
from mnemonic import Mnemonic
from pbkdf2 import PBKDF2
from rng import RNG
import hashlib
import hmac

class BrainWallet:
    # primes slightly larger than a power of 2
    BIGGER_PRIMES={128:2**128+51,
                160:2**160+7,
                192:2**192+133,
                224:2**224+735,
                256:2**256+297}

    # primes slightly smaller than a power of 2
    SMALLER_PRIMES={128:2**128-159,
                  160:2**160-47,
                  192:2**192-237,
                  224:2**224-63,
                  256:2**256-189}

    DEFAULT_MINIMUM = 2
    DEFAULT_SHARES  = 4
    DEFAULT_PRIME = SMALLER_PRIMES[128]
    DEFAULT_LANGUAGE = "english"

    def __init__(self):
        self._minimum = None
        self._shares = None
        self._prime = None
        self._language = None
        self._shamir = None
        self._phrases = None
        self._secret = None

    def getMinimum(self):
        return self._minimum if self._minimum != None else self.DEFAULT_MINIMUM
    def setMinimum(self,value):
        if self._shamir != None:
            raise ValueError("shamir already configured")
        if self._minimum != None:
            raise ValueError("minimum already set")
        self._minimum = Check.toInt(value,"minimum",1)

    def getShares(self):
        return self._shares if self._shares != None else self.DEFAULT_SHARES

    def setShares(self,value):
        if self._shamir != None:
            raise ValueError("shamir already configured")
        if self._shares != None:
            raise ValueError("shares already set")
        self._shares = Check.toInt(value,"shares",1)
        
    def getPrime(self):
        return self._prime if self._prime != None else self.DEFAULT_PRIME

    def setBits(self,bits):
        bits=Check.toInt(bits,"bits",128,256)
        self.setPrime(self.SMALLER_PRIMES[bits])

    def setPrime(self,value):
        if self._shamir != None:
            raise ValueError("shamir already configured")
        if self._prime != None:
            raise ValueError("prime already set")
        self._prime = Check.toPrime(value)

    def getLanguage(self):
        return self._language if self._language != None else self.DEFAULT_LANGUAGE

    def setLanguage(self,language):
        language = Check.toString(language)
        if not (language in Phrases.getLanguages()):
            raise ValueError("language missing")
        self._language = language

    def _getShamir(self):
        if self._shamir == None:
            self._shamir = Shamir(self.getMinimum(),self.getShares(),self.getPrime())
            if self._secret != None:
                self._shamir.setSecret(self._secret)
        return self._shamir

    def _getPhrases(self):
        return Phrases.forLanguage(self.getLanguage())

    def number(self,phrase):
        phrase=Check.toString(phrase)
        if self._getPhrases().isPhrase(phrase):
            return self._getPhrases().toNumber(phrase)
        else:
            detected=Phrases.detectLanguage(phrase)
            return Phrases.forLanguage(detected).toNumber(phrase)
                
    def phrase(self,number):
        return self._getPhrases().toPhrase(Check.toInt(number))

    def getSecret(self):
        if self._shamir != None:
            return self.phrase(self._getShamir().getSecret())
        elif self._secret != None:
            return self._secret
        else:
            raise ValueError("secret and recovery keys are not set")

    def setSecret(self,value):
        self._secret = value
        if self._shamir != None:
            self._getShamir().setSecret(self.number(value))

    def getKey(self,index):
        index = Check.toInt(index,"index",1,self.getShares())
        return self.phrase(self._getShamir().getKey(index))

    def setKey(self,index,value):
        index = Check.toInt(index,"index",1,self.getShares())
        self._getShamir().setKey(index,self.number(value))

    def randomize(self):
        self._getShamir().setRandomSecret()
        self._getShamir().makeKeys()

    def recover(self):
        self._getShamir().recoverKeys()

    def seed1(self,salt = ""):
        return Mnemonic.to_seed(self.getSecret(),salt)

    PBKDF2_ROUNDS = 2048
    def seed2(self,salt = ""):
        return PBKDF2(
            self.getSecret(),
            u"mnemonic" + salt,
            iterations=self.PBKDF2_ROUNDS,
            macmodule=hmac,
            digestmodule=hashlib.sha512,
        ).read(64)

    def getSeed(self,salt = ""):
        password=self.getSecret().encode("utf-8")
        salt=(u"mnemonic" + salt).encode("utf-8")
        iterations=self.PBKDF2_ROUNDS
        stretched = hashlib.pbkdf2_hmac('sha512', password, salt, iterations)
        return stretched[0:64]

    def getCheckedSeed(self,passphrase = ""):
        s1=self.seed1(passphrase)
        s2=self.seed2(passphrase)
        s=self.getSeed(passphrase)
        assert s1 == s
        assert s2 == s
        return s

    # Refactored code segments from <https://github.com/keis/base58>
    B58_ALPHABET="123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"

    @classmethod
    def b58encode(cls,data):
        p = 1
        acc = 0
        for c in reversed(data):
            if not Check.PYTHON3:
                c = ord(c)
            acc += p * c
            p = p << 8

        string = ""
        while acc:
            acc, idx = divmod(acc, 58)
            string = cls.B58_ALPHABET[idx : idx + 1] + string
        return string

    @classmethod
    def getCheckedHDMasterKey(cls,seed):
        key1 = Mnemonic.to_hd_master_key(seed)
        key = cls.getHDMasterKey(seed)
        assert key == key1
        return key

    @classmethod
    def getHDMasterKey(cls,seed):
        if len(seed) != 64:
            raise ValueError("Provided seed should have length of 64")

        seed = hmac.new(b"Bitcoin seed", seed, digestmod=hashlib.sha512).digest()

        # Serialization format can be found at: https://github.com/bitcoin/bips/blob/master/bip-0032.mediawiki#Serialization_format
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
        shares = self.getShares()
        minimum = self.getMinimum()
        language = self.getLanguage()

        print ("--language=%s" % language)
        print ("--prime=%d" % prime)
        print ("--minimum=%d" % minimum)
        print ("--shares=%d" % shares)
        print ("--secret=\"%s\"" % self.getSecret())
        for i in range(1,self.getShares()+1):
            print ("--key%d=\"%s\"" % (i,shares,self.getKey(i)))
        print ("Secret can be recovered with any %d of the %d keys" % (minimum, shares))
        print ("Remember the key id (1-%d) and corresponding phrase." % shares)

    def cli(self,args):
        for i in range(len(args)):
            arg=args[i]

            cmd="--language"
            if arg == cmd: print(self.getLanguage())
            if arg.startswith(cmd+"="): self.setLanguage(arg[len(cmd)+1:])

            cmd="--minimum"
            if arg == cmd: print(self.getMinimum())
            if arg.startswith(cmd+"="): self.setMinimum(arg[len(cmd)+1:])

            cmd="--shares"
            if arg == cmd: print(self.getShares())
            if arg.startswith(cmd+"="): self.setShares(arg[len(cmd)+1:])

            cmd="--prime"
            if arg == cmd: print(self.getPrime())
            if arg.startswith(cmd+"="): self.setPrime(arg[len(cmd)+1:])

            cmd="--bits"
            if arg.startswith(cmd+"="): self.setBits(arg[len(cmd)+1:])

            cmd="--secret"
            if arg == cmd: print(self.getSecret().encode('utf-8'))
            if arg.startswith(cmd+"="): self.setSecret(arg[len(cmd)+1:])

            for index in range(1,self.getShares()+1):
                cmd="--key"+str(index)
                if arg == cmd: 
                    print(self.getKey(index).encode('utf-8'))
                if arg.startswith(cmd+"="): 
                    self.setKey(index,arg[len(cmd)+1:])

            cmd="--randomize"
            if arg == cmd: self.randomize()
            cmd="--recover"
            if arg == cmd: self.recover()
            cmd="--dump"
            if arg == cmd: self.dump()
            cmd="--seed"
            if arg == cmd: 
                print (binascii.hexlify(self.getCheckedSeed()))
            cmd="--master"
            if arg == cmd: 
                seed = self.getCheckedSeed()
                key = self.getCheckedHDMasterKey(seed)
                print (key)

def main():
    brainWallet=BrainWallet()
    brainWallet.cli(sys.argv[1:])

if __name__ == "__main__":
    main()
