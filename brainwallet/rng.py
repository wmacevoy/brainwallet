import sys
import os
import math

class RNG:
    def __init__(self,source = os.urandom):
        self.source = source

    _BITS=dict()

    @classmethod
    def _bits(cls,n):
        if n in cls._BITS: return cls._BITS[n]
        bits = int(math.ceil(math.log(int(n),2)))
        # fix inexact results of float math
        while 2**bits < n:
            bits = bits + 1
        while 2**(bits-1) > n:
            bits = bits - 1

        cls._BITS[n]=bits
        return bits

    def next(self,n):
        ''' uniformly random value [0,n-1] derived from source '''
        bits = self._bits(n)
        bytes = (bits + 7)//8
        mask = 2**bits - 1
        while True:
            data = self.source(bytes)
            k = 0
            for i in range(bytes):
                bi = ord(data[i:i+1])
                k = k | (bi << (8*i))
            k = k & mask
            if k < n: return k

def main():
    rng = RNG()
    for i in range(1,len(sys.argv)):
        print(rng.next(int(sys.argv[i])))

if __name__ == "__main__":
    main()
