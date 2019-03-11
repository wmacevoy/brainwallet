import sys
import os
import math

class RNG:
    def __init__(self,source = os.urandom):
        self.source = source

    def next(self,n):
        ''' uniformly random value [0,n-1] derived from source '''
        bits = int(math.ceil(math.log(n,2)))
        while 2**bits < n:
            bits = bits + 1

        if bits % 8 != 0:
            bytes = bits/8 + 1
        else:
            bytes = bits/8

        mask = 2**bits-1

        ok = False
        while not ok:
            data = self.source(bytes)
            k = 0
            for i in xrange(bytes):
                bi = ord(data[i])
                k = k | (bi << (8*i))
            k = k & mask
            ok = k < n
        return k

def main():
    rng = RNG()
    for i in xrange(1,len(sys.argv)):
        print rng.next(int(sys.argv[i]))

if __name__ == "__main__":
    main()
