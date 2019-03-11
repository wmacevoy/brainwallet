import math
import struct

class RNG:
    def __init__(self):
        self.dev = open("/dev/random", 'rb')
        self.struct = struct.Struct('B')

    def next(self,n):
        bits=int(math.ceil(math.log(n,2)))
        while 2**bits < n:
            bits = bits + 1

        if bits % 8 != 0:
            bytes = bits/8 + 1
        else:
            bytes = bits/8

        mask = 2**bits-1

        ok = False
        while not ok:
            data = self.dev.read(bytes)
            k = 0
            for i in xrange(bytes):
                bi = self.struct.unpack_from(data,i)[0]
                k = k | (bi << (8*i))
            k = k & mask
            ok = k < n
        return k

def main:
    print rng.next(2**127)

if __name__ == "__main__":
    main()

