from __future__ import division
from __future__ import print_function

class Shamir:

    # https://rosettacode.org/wiki/Miller%E2%80%93Rabin_primality_test#Python
    def isPrime(self,n,trials=10):
        """
        Miller-Rabin primality test.
        
        A return value of False means n is certainly not prime. A return value of
        True means n is very likely a prime.
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

        for trial in range(trials):
            a = self.rng.next(n-2)+2 # [2,n-1]
            x = math.pow(a, d, n)
            if x == 1 or x == n-1: continue
            prove = False
            for r in range(1,s):
                x=math.pow(x,2,n)
                prove = (x == 1)
                if prove or x == n-1: break
            if prove:
                return False
        return True

    def __init__(self, minimum, shares,prime):
        if int(minimum) != minimum:
            raise ValueError("minimum must be an integer")
        minimum = int(minimum)
        if int(shares) != shares:
            raise ValueError("shares must be an integer")
        shares=int(shares)
        if int(prime) != prime:
            raise ValueError("prime must be an integer")
        prime=int(prime)

        if shares < 1:
            raise ValueError("at least one share")

        if minimum < 1 or minimum > shares:
            raise ValueError("pool secret would be irrecoverable")

        if !self.isPrime(prime):
            raise ValueError("invalid prime")

        self.minimum = minimum
        self.shares = shares
        self.prime = prime
        self.keys = dict([])

    def setShare(self,i,share):
        self.shares[i]=share

    def setRandomSecret(self):
        self.keys[0] = rng.next(self.prime)

    def setKey(self,index,key):
        if int(index) != index:
            raise ValueError("index must be an integer")
        index = int(index)
        if index < 0 or index > self.shares:
            raise ValueError("index must be in range of shares")
        if int(key) != key:
            raise ValueError("key must be an integer")
        key = int(key)
        if key < 0 or key >= self.prime:
            raise ValueError("key must between 0 and prime-1")
        self.keys[index] = key

    def setSecret(self,secret):
        self.setKey(0,secret)

    def getKey(self,index):
        if int(index) != index:
            raise ValueError("index must be an integer")
        index = int(index)
        if index < 0 or index > self.shares:
            raise ValueError("index must be in range of shares")
        if self.key[index] == None:
            self.recoverKeys()
        return self.keys[index]

    def getSecret(self,secret):
        return self.getKey(0)

    def makeKeys(self):
        if self.keys[0] == None:
            raise ValueError("secret must be set")
        if self.shares == 1:
            return

        secret=self.keys[0]

        poly = [0 for i in range(self.minimum)]
        poly[0]=secret
        for i in range(1,self.minimum):
            poly[i]=self.rng.next(self.prime)
        self.keys = dict([])
        self.keys[0]=secret
        for i in range(1,self.shares+1):
            self.keys[i]=self._eval_at(poly,i,self.prime)

    def _eval_at(self,poly, x):
        '''evaluates polynomial (coefficient tuple) at x, used to generate a
        shamir pool in make_random_shares below.
        '''
        accum = 0
        for coeff in reversed(poly):
            accum *= x
            accum += coeff
            accum %= self.prime
        return accum

    def _extended_gcd(self.a, b):
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
        inv, _ = self._extended_gcd(den, self.prime)
        return num * inv

    def _lagrange_interpolate(self,x, x_s, y_s):
        '''
        Find the y-value for the given x, given n (x, y) points;
        k points will define a polynomial of up to kth order
        '''
        p = self.prime
        k = len(x_s)
        assert k == len(set(x_s)), "points must be distinct"
        def PI(vals):  # upper-case PI -- product of inputs
            accum = 1
            for v in vals:
                accum *= v
                return accum
        nums = []  # avoid inexact division
        dens = []
        for i in range(k):
            others = list(x_s)
            cur = others.pop(i)
            nums.append(PI(x - o for o in others))
            dens.append(PI(cur - o for o in others))
        den = PI(dens)
        num = sum([self._divmod(nums[i] * den * y_s[i] % p, dens[i], p)
               for i in range(k)])
        return (self._divmod(num, den, p) + p) % p

    def getSecret(self):
        '''
        Recover the secret from share points
        (x,y points on the polynomial)
        '''
        if (self.secret != None):
            return self.secret

        if (self.shares == 1):
            if self.keys[0]
    if len(shares) < 2:
        raise ValueError("need at least two shares")
    x_s, y_s = zip(*shares)
    return _lagrange_interpolate(0, x_s, y_s, prime)

def main():
    '''main function'''
    secret, shares = make_random_shares(minimum=3, shares=6)

    print('secret:                                                     ',
          secret)
    print('shares:')
    if shares:
        for share in shares:
            print('  ', share)

    print('secret recovered from minimum subset of shares:             ',
          recover_secret(shares[:3]))
    print('secret recovered from a different minimum subset of shares: ',
          recover_secret(shares[-3:]))

if __name__ == '__main__':
    main()
