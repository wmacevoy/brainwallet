#!/usr/bin/env python

from rng import RNG
from check import Check


class Shamir:
    def __init__(self, minimum, prime):
        if minimum != None:
            minimum = Check.toInt(minimum, "minimum", 1)
        prime = Check.toPrime(prime)

        self._minimum = minimum
        self._prime = prime
        self._keys = dict()

    def getMinimum(self):
        return self._minimum

    def getPrime(self):
        return self._prime

    def setKey(self, index, key):
        index = Check.toInt(index, "index", 0)
        name = "key" if index > 0 else "secret"
        key = Check.toInt(key, name, 0, self._prime - 1)
        self._keys[index] = key

    def randomizeSecret(self, rng=RNG()):
        self.setSecret(rng.next(self._prime))

    def setSecret(self, secret):
        self.setKey(0, secret)

    def getSecret(self):
        return self.getKey(0)

    def randomizeKeys(self, shares, rng=RNG()):
        shares = Check.toInt(shares, "shares", self._minimum)

        if self._keys[0] is None:
            raise ValueError("secret must be set")
        if self._minimum is None:
            raise ValueError("minimum must be set")
        secret = self._keys[0]

        cs = [0 for i in range(self._minimum)]
        cs[0] = secret
        for i in range(1, self._minimum):
            cs[i] = rng.next(self._prime)
        self._keys = dict()
        self._keys[0] = secret
        for i in range(1, shares + 1):
            self._keys[i] = self._evalPoly(cs, i)

    def _evalPoly(self, cs, x):
        '''evaluates polynomial (coefficient tuple) at x'''
        a = 0
        for c in reversed(cs):
            a *= x
            a += c
            a %= self._prime
        return a

    @classmethod
    def _extendedGCD(cls, a, b):
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
            a, b = b, a % b
            x, lastX = lastX - quot * x, x
            y, lastY = lastY - quot * y, y
        return lastX, lastY

    def _divmod(self, num, den):
        '''compute num / den modulo prime'''
        num = num % self._prime
        den = den % self._prime
        inv, _ = self._extendedGCD(den, self._prime)
        return (num * inv) % self._prime

    def _PI(self, vals):
        a = 1
        for v in vals:
            if v < 0:
                v = self._prime + v
            a = (a * v) % self._prime
        return a

    def _lagrangeInterpolate(self, x, xs, ys):
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

    def getKey(self, index):
        index = Check.toInt(index, "index", 0)
        if index not in self._keys:
            xs = []
            ys = []
            for x in self._keys:
                xs.append(x)
                ys.append(self._keys[x])
#                if len(xs) == self._minimum:
#                    break

            if self._minimum != None and len(xs) < self._minimum:
                raise ValueError("only %d of minimum %s keys" %
                                 (len(xs), self._minimum))

            self._keys[index] = self._lagrangeInterpolate(index, xs, ys)
        return self._keys[index]
