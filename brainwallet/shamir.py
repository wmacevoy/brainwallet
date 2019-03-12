#!/usr/bin/env python

from rng import RNG
from check import Check


class Shamir:
    def __init__(self, minimum, shares,prime,rng=RNG()):
        shares = Check.toInt(shares,"shares",1)
        minimum = Check.toInt(minimum,"minimum",1,shares)
        prime = Check.toPrime(prime)

        self._rng = rng
        self._minimum = minimum
        self._shares = shares
        self._prime = prime
        self._keys = [None]*(self._shares+1)

    def getMinimum(self):
        return self._minimum

    def getShares(self):
        return self._shares

    def getPrime(self):
        return self._prime

    def setKey(self,index,key):
        index=Check.toInt(index,"index",0,self._shares)
        name="key" if index > 0 else "secret"
        key=Check.toInt(key,name,0,self._prime-1)
        self._keys[index] = key

    def clearKey(self,index):
        index=Check.toInt(index,"index",0,self._shares)
        name="key" if index > 0 else "secret"
        self._keys[index] = None

    def setRandomSecret(self):
        self.setSecret(self._rng.next(self._prime))

    def setSecret(self,secret):
        self.setKey(0,secret)

    def getKey(self,index):
        index=Check.toInt(index,"index",0,self._shares)
        if self._keys[index] == None:
            self.recoverKeys()
        return self._keys[index]

    def getSecret(self):
        return self.getKey(0)

    def makeKeys(self):
        if self._keys[0] == None:
            raise ValueError("secret must be set")
        secret=self._keys[0]

        cs = [0 for i in range(self._minimum)]
        cs[0]=secret
        for i in range(1,self._minimum):
            cs[i]=self._rng.next(self._prime)
        self._keys[0]=secret
        for i in range(1,self._shares+1):
            self._keys[i]=self._evalPoly(cs,i)

    def _evalPoly(self,cs, x):
        '''evaluates polynomial (coefficient tuple) at x'''
        a = 0
        for c in reversed(cs):
            a *= x
            a += c
            a %= self._prime
        return a

    @classmethod
    def _extendedGCD(cls,a,b):
        '''
        division in integers modulus p means finding the inverse of the
        denominator modulo p and then multiplying the numerator by this
        inverse (Note: inverse of A is B such that A*B % p == 1) this can
        be computed via extended Euclidean algorithm
        http://en.wikipedia.org/wiki/Modular_multiplicative_inverse#Computation
        '''
        x = 0
        lastX = 1
        y = 1
        lastY = 0
        while b != 0:
            quot = a // b
            a, b = b, a%b
            x, lastX = lastX - quot * x, x
            y, lastY = lastY - quot * y, y
        return lastX, lastY
        
    def _divmod(self,num, den):
        '''compute num / den modulo prime'''
        num = num % self._prime
        den = den % self._prime
        inv, _ = self._extendedGCD(den, self._prime)
        return (num * inv) % self._prime

    def _PI(self,vals):
        a = 1
        for v in vals:
            if v < 0: v = self._prime + v
            a = (a*v) % self._prime
        return a
        
    def _lagrangeInterpolate(self,x, xs, ys):
        '''
        Find the y-value for the given x, given n (x, y) points;
        k points will define a polynomial of up to kth order
        '''
        k = len(xs)
        assert k == len(set(xs)), "points must be distinct"

        nums = []
        dens = []
        
        for i in range(k):
            others = list(xs)
            cur = others.pop(i)
            nums.append(self._PI(x - o for o in others))
            dens.append(self._PI(cur - o for o in others))

        den = self._PI(dens)
        num = sum([self._divmod(nums[i] * den * ys[i], dens[i])
               for i in range(k)])
        return self._divmod(num, den)

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
                self._keys[i]=self._lagrangeInterpolate(i,xs,ys)

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
