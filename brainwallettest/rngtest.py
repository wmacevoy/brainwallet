import inspect
import math
import os
import sys
import unittest

currentdir = os.path.dirname(
    os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)

sys.path.insert(0, parentdir + "/brainwallet")

import rng

class RNGTest(unittest.TestCase):
    def getUnit(self):
        return rng.RNG()

    def _testRange(self, b, n):
        rng = self.getUnit()
        counts = [0 for x in range(b)]
        for t in range(n):
            x = rng.next(b)
            assert x == int(x) and x >= 0 and x < b
            counts[x] += 1

        probabilityOfError = 1e-20
        p = float(1) / float(b)
        q = float(b - 1) / float(b)
        mu = n * p
        sigma = math.sqrt(n * p * q)
        delta = sigma * self.approxInvErf(probabilityOfError)
        for x in range(b):
            assert abs(counts[x] - mu) < delta

    def testRanges(self):
        n = 12345
        for b in range(2, 1100, 13):
            self._testRange(b, n)

    @classmethod
    def approxInvErf(cls, eps):
        b = (3.0 * math.pi * (4.0 - math.pi)) / (8.0 * (math.pi - 3.0))
        sigma = math.copysign(1.0, eps)
        eps = abs(eps)
        t = math.log(eps * (2.0 - eps))
        Q = (2.0 * b) / math.pi + 0.5 * t
        y = math.sqrt(Q * Q - t * b) - Q
        return math.copysign(math.sqrt(y), sigma)

    def testInvErf(self):
        self.assertClose("ierf(1-erf(2))", self.approxInvErf(0.00467773), "2",
                         2, abs_tol=1, rel_tol=1e-2)
        self.assertClose("ierf(1-erf(6))", self.approxInvErf(2.151e-17), "6",
                         6, abs_tol=1, rel_tol=1e-2)

    # adapted from
    # (https://stackoverflow.com/questions/12136762/assertalmostequal-in-
    #  python-unit-test-for-collections-of-floats)
    @classmethod
    def assertClose(cls, aname, a, bname, b, rel_tol=1e-9, abs_tol=0.0):
        if abs(a - b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol):
            return
        raise ValueError(str(aname) + "=" + str(a) + "is not close to " +
                         str(bname) + "=" + str(b) + " with rel_tol=" +
                         str(rel_tol) + " and abs_tol=" + str(abs_tol))


if __name__ == '__main__':
    unittest.main()
