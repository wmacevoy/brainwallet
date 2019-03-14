import inspect,math,os,sys,unittest

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)

sys.path.insert(0,parentdir+"/brainwallet") 

from millerrabin import MillerRabin
from shamir import Shamir
from rng import RNG

class ShamirTest(unittest.TestCase):
    def _testShamirRecover(self,minimum,shares,prime,secret,keys):
        shamir = Shamir(minimum,shares,prime)
        choices=list(range(shares))
        rng = RNG()
        for k in range(minimum):
            i=rng.next(len(choices))
            shamir.setKey(choices[i]+1,keys[choices[i]])
            del choices[i]
                
        shamir.recoverKeys()
        assert shamir.getSecret() == secret
        for i in range(shares):
            assert shamir.getKey(i+1) == keys[i]

    def _testShamir(self,minimum,shares,prime,secret):
        shamir = Shamir(minimum,shares,prime)
        shamir.setSecret(secret)
        shamir.randomizeKeys()
        keys=[shamir.getKey(i) for i in range(1,shares+1)]
        for t in range(100):
            self._testShamirRecover(minimum,shares,prime,secret,keys)

    def testShamir(self):
        rng = RNG()
        millerrabin = MillerRabin()
        for bits in range(32,256,4):
            prime = millerrabin.prevPrime(2**bits)
            for shares in range(1,9):
                for minimum in range(1,shares+1):
                    for secret in [0,1,2,rng.next(prime),prime-2,prime-1]:
                        self._testShamir(minimum,shares,prime,secret)

if __name__ == '__main__':
    unittest.main()
