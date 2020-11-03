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
        return t

    @classmethod
    def unrank(cls,n,r,k):
        j=k
        c=[0]*r
        for i in range(r):
            if i > 0:
                hi=c[i-1]
            else:
                hi=n
            lo=r-i-1
            while hi-lo > 1:
                mid=(lo+hi)//2
                if cls.choose(mid,r-i) <= j:
                    lo=mid
                else:
                    hi=mid
            c[i]=lo
            j -= cls.choose(c[i],r-i)
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
    print("no main")

if __name__ == "__main__":
    main()
