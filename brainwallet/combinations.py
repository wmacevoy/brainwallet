import sys
import os
import math

#
# https://en.wikipedia.org/wiki/Combinatorial_number_system
#

def choose(n,r):
    """
    number of combinations of n things taken r at a time (order unimportant)
    """
    if n < 0:
        raise ValueError("invalid parameters")
    
    s = min(r, n - r)
    if s <= 0:
        return 1 if s == 0 else 0
    t = n
    a = n-1
    b = 2
    while b <= s:
        t = (t*a)//b
        a -= 1
        b += 1
    return t

def unrank(n,r,k):
    """
    k, the rank, is in the range 0..combinations(n,r)-1
    assuming combinations listed in increasing lexicographic order,
    returns c=[c_0, .. c_(r-1)] with c_0 > c_1 ..., which is the 
    kth combination in the list (starting with 0)
    """
    if k < 0 or k >= choose(n,r):
        raise ValueError("invalid parameters")
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
            if choose(mid,r-i) <= j:
                lo=mid
            else:
                hi=mid
        c[i]=lo
        j -= choose(c[i],r-i)
    return c

def rank(n,r,c):
    d = sorted(c,reverse = True)
    if n < 0 or r < 0 or r > n or len(d)!= r:
        raise ValueError("invalid parameter")
    for i in range(r):
        if d[i] < 0 or n <= d[i] or (i > 0 and d[i] == d[i-1]):
            raise ValueError("invalid parameter")
    k=0
    for i in range(r):
        k +=  choose(d[i],r-i)
    return k

def main():
    print("no main")

if __name__ == "__main__":
    main()
