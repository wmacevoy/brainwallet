#!/usr/bin/env python

import inspect,math,os,sys,unittest

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)

sys.path.insert(0,parentdir+"/brainwallet") 

from millerrabin import MillerRabin
from shamir import Shamir
from rng import RNG

class ShamirTest(unittest.TestCase):
    rng = RNG()
    debug = 0
    def _testShamirRecover(self,minimum,shares,prime,secret,keys):
        if self.debug >= 100:
            print("testShamirRecover(minimum=%d,shares=%d,prime=%d,secret=%s,keys=%s)" % (minimum,shares,prime,secret,keys))
        shamir = Shamir(minimum,prime)
        choices=list(range(shares))
        for k in range(minimum):
            i=self.rng.next(len(choices))
            shamir.setKey(choices[i]+1,keys[choices[i]])
            del choices[i]
                
        assert shamir.getSecret() == secret
        for i in range(shares):
            assert shamir.getKey(i+1) == keys[i]

    def _testShamir(self,minimum,shares,prime,secret):
        if self.debug >= 10:
            print("testShamir(minimum=%d,shares=%d,prime=%d,secret=%d)" % (minimum,shares,prime,secret))
        shamir = Shamir(minimum,prime)
        shamir.setSecret(secret)
        shamir.randomizeKeys(shares,self.rng)
        keys=[shamir.getKey(i) for i in range(1,shares+1)]
        for t in range(100):
            self._testShamirRecover(minimum,shares,prime,secret,keys)

    def testShamir(self):
        if self.debug >= 1:
            print("testShamir()")
        millerrabin = MillerRabin()
        for bits in range(32,256,4):
            prime = millerrabin.prevPrime(2**bits)
            for shares in range(1,9):
                for minimum in range(1,shares+1):
                    for secret in [0,1,2,self.rng.next(prime),prime-2,prime-1]:
                        self._testShamir(minimum,shares,prime,secret)

if __name__ == '__main__':
    unittest.main()

