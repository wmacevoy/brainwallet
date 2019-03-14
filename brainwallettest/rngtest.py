import inspect,math,os,sys,unittest

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)

sys.path.insert(0,parentdir+"/brainwallet") 

import rng

class RNGTest(unittest.TestCase):
    def getUnit(self):
        return rng.RNG()

    def _testRange(self,b,n):
        rng = self.getUnit()        
        counts = [0 for x in range(b)]
        for t in range(n):
            x = rng.next(b)
            assert x == int(x) and x >= 0 and x < b
            counts[x] += 1
            
        probabilityOfError = 1e-20;
        mu=float(n)/float(b)
        sigma=math.sqrt(float(n)/float(b)*float(b-1)*float(b))
        delta=math.sqrt(2.0)*sigma*self.approxInvErf(probabilityOfError)
        for x in range(b):
            assert abs(counts[x]-mu)<delta

    def testRanges(self):
        n = 12345
        for b in range(2,1100,13):
            self._testRange(b,n)

    @classmethod
    def approxInvErf(cls,eps):
        b=(3.0*math.pi*(4.0-math.pi))/(8.0*(math.pi-3.0))
        sigma=math.copysign(1.0,eps)
        eps=abs(eps);
        t=math.log(eps*(2.0-eps))
        Q=(2.0*b)/math.pi+0.5*t;
        y=math.sqrt(Q*Q-t*b)-Q
        return math.copysign(math.sqrt(y),sigma)

if __name__ == '__main__':
    unittest.main()
