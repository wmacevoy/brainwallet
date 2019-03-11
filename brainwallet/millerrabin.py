# adapted from
#
# https://rosettacode.org/wiki/Miller%E2%80%93Rabin_primality_test#Python
#
import sys
import math
from rng import RNG

class MillerRabin:
    def __init__(self,trials=10,rng=RNG()):
        self.trials = trials
        self.rng = rng

    def isProbablyPrime(self,n):
        """
        Miller-Rabin primality test.
    
        A return value of False means n is certainly not prime.
        A return value of True means n is very likely a prime.
        """

        if n!=int(n):
            return False

        n=int(n)

        if n<2:
            return False
 
        if n==2 or n==3 or n==5:
            return True

        if n % 2 == 0 or n % 3 == 0 or n % 5 == 0:
            return False
    
        # write n-1 as (2**s)*d
        s = 0
        d = n-1
        while d%2==0:
            d>>=1
            s+=1

        for trial in xrange(self.trials):
            a = self.rng.next(n-2)+2 # [2,n-1]
            x = pow(a, d, n)
            if x == 1 or x == n-1: continue
            prove = False
            for r in range(1,s):
                x=pow(x,2,n)
                prove = (x == 1)
                if prove or x == n-1: break
            if prove:
                return False
        return True

def main():
    mr = MillerRabin()
    for i in xrange(1,len(sys.argv)):
        x = int(sys.argv[i])
        q = mr.isProbablyPrime(x)
        print "prime(" + str(x) +")=" + str(q)

if __name__ == "__main__":
    main()
