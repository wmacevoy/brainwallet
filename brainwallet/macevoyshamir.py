#!/usr/bin/env python

from rng import RNG
from check import Check


# Use points [-(m-1),..,0] as extended secret points
 class MacEvoyShamir:
    def __init__(self, minimum, prime):
        prime = Check.toPrime(prime)
        minimum = Check.toInt(minimum,"minimum",1,prime // 2 - 1)
        self._minimum = minimum
        self._prime = prime
        self._points = dict()

    def getMinimum(self):
        return self._minimum

    def getPrime(self):
        return self._prime

    def setPoint(self,index,value):
        index=Check.toInt(index,"index")
        name="share" if index > 0 else "secret"
        key=Check.toInt(key,name,0,self._prime-1)
        if (len(self._points) >= self._minimum):
            assert self.getPoint(index) == value
        self._points[index] = value

    def randomizeSecrets(self,rng=RNG()):
        self._points = dict()
        for index in range(self.getMinimum()):
            secret=rng.next(self._prime)
            self.setSecret(index,value)

    def setSecret(self,index,secret):
        index=Check.toInt(index,"secret",0,self._minimum - 1)
        self.setPoint((self._prime-index) % self._prime,secret)

    def getSecret(self,index):
        index=Check.toInt(index,"secret",0,self._minimum - 1)
        return self.getPoint((self._prime-index) % self._prime)

    def setShare(self,index,secret):
        index=Check.toInt(index,"share",1,self._prime // 2 - 1)
        self.setPoint(index,secret)

    def getShare(self,index):
        index=Check.toInt(index,"share",1,self._prime // 2 - 1)
        return self.getPoint(index)

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

    def getPoint(self,index):
        index = index % self._prime
        if index > self.getPrime()//2:
            index=index-self.getPrime()
        index = Check.toInt(index,"index",-self._minimum+1)
        if index in self._points: return self._points[index]

        xs=[]
        ys=[]
        for x in self._points:
            xs.append(x)
            ys.append(self._points[x])
            if len(xs) == self._minimum: break

        if len(xs) < self._minimum:
            raise ValueError("only %d of minimum %s points" % (len(xs),self._minumum))

        self._points[index]=self._lagrangeInterpolate(index % self._prime,xs,ys)
        return self._points[index]
