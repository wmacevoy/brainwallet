import sys
import os
import math

# https://en.wikipedia.org/wiki/Combinatorial_number_system
class Combinations:
    def __init__(self,n,r):
        self._n = n
        self._r = r

    @classmethod
    def choose(cls,n,r):
        """nCr"""
        if (n < r):
            return 0
        if (n == r):
            return 1
        s = min(r, (n - r))
        t = n
        a = n-1
        b = 2
        while b <= s:
            t = (t*a)//b
            a -= 1
            b += 1
            
        print("choose(" + str(n) + "," + str(r) + ")=" + str(t))
        return t

    @classmethod
    def _largestV(cls,a,b,x):
        v = a - 1;
        print("largestV(" + str(a) + "," + str(b) + "," + str(x) + ")")        
        while (cls.choose(v, b) > x):
            v -= 1
        print("largestV(" + str(a) + "," + str(b) + "," + str(x) + ")=" + str(v))
        return v

    @classmethod
    def _combinadic(cls,n,r,k):
        """
        Finds the combinadic of k for nCr.
        
        Combinadic of k corresponds to the array of [c_1, c_2, ..., c_r] such
        that k = choose(c_1, r) + choose(c_2, r-1) + ... + choose(c_r, 1).
        """
        x = k
        a = n
        b = r
        c = [0]*r
        print("combinadic(" + str(n) + "," + str(r) + "," + str(k) + ")")
        for i in range(r):
            c[i] = cls._largestV(a, b, x)
            x -= cls.choose(c[i], b)
            a = c[i]
            b -= 1
        print("combinadic(" + str(n) + "," + str(r) + "," + str(k) + ")=" + str(c))            
        return c

    @classmethod
    def unrank(cls,n,r,k):
        nCr = cls.choose(n, r)
        if (nCr == 0):
            return
        d = nCr - k - 1
        c=cls._combinadic(n, r, d)
        for i in range(r):
            c[i] = n - c[i] - 1
        return c
    
    @classmethod    
    def rank(cls,n,r,c):
        d = [c[i] for i in range(r)]
        d.sort(reverse=True)
        k=0
        for i in range(r):
           k +=  cls.choose(d[i],r-i)
        return k

def main():
    
    rng = RNG()
    for i in range(1,len(sys.argv)):
        print(rng.next(int(sys.argv[i])))

if __name__ == "__main__":
    main()
