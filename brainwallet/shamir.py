#!/usr/bin/env python

from __future__ import division
from __future__ import print_function
from rng import RNG
from millerrabin import MillerRabin

class Shamir:
    _RNG=RNG()
    _MILLER_RABIN=MillerRabin(10,_RNG)
    _PRIMES=set()

    @classmethod
    def isPrime(cls,n):
        if n in cls._PRIMES: return True
        if cls._MILLER_RABIN.isProbablyPrime(n):
            cls._PRIMES.add(n)
            return True
        return False

    @classmethod
    def _toInt(cls,n,name=None,min=None,max=None):
        if name == None:
            name = "value"
        if int(n) != n:
            raise ValueError(str(name) + " must be an integer")
        n = int(n)
        if min != None and n < min:
            raise ValueError(str(name) + " must be >= " + str(min))
        if max != None and n > max:
            raise ValueError(str(name) + " must be <= " + str(max))
        return n

    def __init__(self, minimum, shares,prime,rng=RNG()):
        shares = Shamir._toInt(shares,"shares",1)
        minimum = Shamir._toInt(minimum,"minimum",1,shares)
        if not Shamir.isPrime(prime):
            raise ValueError("invalid prime")

        self._rng = rng
        self._minimum = minimum
        self._shares = shares
        self._prime = prime
        self._keys = [None for i in range(0,self._shares+1)]

    def setKey(self,index,key):
        index=self._toInt(index,"index",0,self._shares)
        name="key" if index > 0 else "secret"
        key=self._toInt(key,name,0,self._prime-1)
        self._keys[index] = key

    def clearKey(self,index):
        index=self._toInt(index,"index",0,self._shares)
        name="key" if index > 0 else "secret"
        self._keys[index] = None

    def setRandomSecret(self):
        self.setSecret(self._rng.next(self._prime))

    def setSecret(self,secret):
        self.setKey(0,secret)

    def getKey(self,index):
        index=Shamir._toInt(index,"index",0,self._shares)
        if self._keys[index] == None:
            self.recoverKeys()
        return self._keys[index]

    def getSecret(self):
        return self.getKey(0)

    def makeKeys(self):
        if self._keys[0] == None:
            raise ValueError("secret must be set")
        if self._shares == 1:
            return

        secret=self._keys[0]

        poly = [0 for i in range(self._minimum)]
        poly[0]=secret
        for i in range(1,self._minimum):
            poly[i]=self._rng.next(self._prime)
        self._keys[0]=secret
        for i in range(1,self._shares+1):
            self._keys[i]=self._eval_at(poly,i)

    def _eval_at(self,poly, x):
        '''evaluates polynomial (coefficient tuple) at x, used to generate a
        shamir pool in make_random_shares below.
        '''
        accum = 0
        for coeff in reversed(poly):
            accum *= x
            accum += coeff
            accum %= self._prime
        return accum

    def _extended_gcd(self,a,b):
        '''
        division in integers modulus p means finding the inverse of the
        denominator modulo p and then multiplying the numerator by this
        inverse (Note: inverse of A is B such that A*B % p == 1) this can
        be computed via extended Euclidean algorithm
        http://en.wikipedia.org/wiki/Modular_multiplicative_inverse#Computation
        '''
        x = 0
        last_x = 1
        y = 1
        last_y = 0
        while b != 0:
            quot = a // b
            a, b = b, a%b
            x, last_x = last_x - quot * x, x
            y, last_y = last_y - quot * y, y
        return last_x, last_y
        
    def _divmod(self,num, den):
        '''compute num / den modulo prime
        
        To explain what this means, the return value will be such that
        the following is true: den * _divmod(num, den, p) % p == num
        '''
        inv, _ = self._extended_gcd(den, self._prime)
        return num * inv

    def _PI(self,vals):
        a = 1
        for v in vals:
            if v < 0: v = self._prime + v
            a = (a*v) % self._prime
        return a
        
    def _lagrange_interpolate(self,x, x_s, y_s):
        '''
        Find the y-value for the given x, given n (x, y) points;
        k points will define a polynomial of up to kth order
        '''
        p = self._prime
        k = len(x_s)
        assert k == len(set(x_s)), "points must be distinct"

        nums = []
        dens = []
        
        for i in range(k):
            others = list(x_s)
            cur = others.pop(i)
            nums.append(self._PI(x - o for o in others))
            dens.append(self._PI(cur - o for o in others))

        den = self._PI(dens)
        num = sum([self._divmod(nums[i] * den * y_s[i] % p, dens[i])
               for i in range(k)])

        return (self._divmod(num, den) + p) % p

    def recoverKeys(self):
        xs=[]
        ys=[]
        x=0
        for key in self._keys:
            if key != None:
                xs.append(x)
                ys.append(key)
                if len(xs) == self._minimum: break
            x+=1
        if len(xs) < self._minimum:
            raise ValueError("insufficient keys")

        for i in xrange(0,self._shares+1):
            if self._keys[i] == None:
                self._keys[i]=self._lagrange_interpolate(i,xs,ys)

def main():
    prime = 2**256 - 2**32 - 2**9 - 2**8 - 2**7 - 2**6 - 2**4 - 1
    rng=RNG()
    for shares in range(1,9):
        for minimum in range(1,shares+1):
            for secret in [0,1,2,rng.next(prime),prime-2,prime-1]:
                shamir = Shamir(minimum,shares,prime)
                shamir.setSecret(secret)
                assert shamir.getSecret() == secret, "before make keys"
                shamir.makeKeys()
                assert shamir.getSecret() == secret, "after make keys"
                keys=[shamir.getKey(i) for i in range(shares+1)]
                for tests in range(100):
                    shamir1 = Shamir(minimum,shares,prime)
                    choices=list(range(1,shares+1))
                    for k in range(minimum):
                        i=rng.next(len(choices))
                        shamir1.setKey(choices[i],keys[choices[i]])
                        del choices[i]

                    shamir1.recoverKeys()

                    keys1=[shamir1.getKey(i) for i in range(shares+1)]
                    if keys1 != keys:
                        print (str(keys1) + " != " + str(keys))
                        raise ValueError("test failed.")

if __name__ == '__main__':
    main()
