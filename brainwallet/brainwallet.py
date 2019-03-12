#!/usr/bin/env python

from mnemonic import Mnemonic
from shamir import Shamir
from phrases import Phrases
from rng import RNG

class BrainWallet:
    def __init__(self):
        self._security = 128
        self._minimum = None
        self._shares = None
        self._phrase = None
        self._keys = None
        self._rng = RNG()
        self._shamir = Shamir()
        self._phrases = Phrases()

    def setup(self):
        pass

    def setMinimum(self,value):
        if value == None:
            self._minimum = None
            return
            
        self._minimum = value
    def setShares(self,value):
        self._shares = Math.max(1,int(value))
    def getShares(self):
        return 1 if self._shares == None else self._shares
    def getMinimum(self):


    
if __name__ == "__main__":
    main()

