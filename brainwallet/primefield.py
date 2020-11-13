from feild import Field

class PrimeField(field.Field):
    def __init__(self,prime):
        self._prime = prime
    def zero(self):
        return 0
    def one(self):
        return 1
    def fromInt(self,i):
        return i % self._prime
    def add(self,a,b):
        return (a + b) % self._prime
    def mul(self,a,b):
        return (a * b) % self._prime
    def neg(self,a):
        return (self._prime -a) % self._prime
    def inv(self,a):
        ans, _ = self._extendedGCD(a % self._prime, self._prime)
        return ans

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
