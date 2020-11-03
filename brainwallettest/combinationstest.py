#!/usr/bin/env python

import inspect,math,os,sys,unittest,time

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)

sys.path.insert(0,parentdir+"/brainwallet") 

import combinations

class CombinationsTest(unittest.TestCase):

    def _testChoose(self,n,r,c):
        nCr=combinations.choose(n,r)
        self.assertEqual(nCr,len(c))

    def _testUnrank(self,n,r,c):
        nCr=combinations.choose(n,r)
        for k in range(nCr):
            d = combinations.unrank(n,r,k)
            self.assertEqual(d,c[k])

    def _testRank(self,n,r,c):
        nCr=combinations.choose(n,r)        
        for k in range(nCr):
            j = combinations.rank(n,r,c[k])
            self.assertEqual(k,j)

    def get5C2(self):
        return [[1, 0], [2, 0], [2, 1], [3, 0], [3, 1], [3, 2], [4, 0], [4, 1], [4, 2], [4, 3]]

    def get5C3(self):
        return [[2, 1, 0],[3, 1, 0],[3, 2, 0],[3, 2, 1],[4, 1, 0],[4, 2, 0],[4, 2, 1],[4, 3, 0],[4, 3, 1],[4, 3, 2]]

    def test5C2Choose(self):
        n=5
        r=2
        c=self.get5C2()
        self._testChoose(n,r,c)

    def test5C2Rank(self):
        n=5
        r=2
        c=self.get5C2()
        self._testRank(n,r,c)

    def test5C2Unrank(self):
        n=5
        r=2
        c=self.get5C2()
        self._testUnrank(n,r,c)
        
    def test5C3Choose(self):
        n=5
        r=3
        c=self.get5C3()
        self._testChoose(n,r,c)

    def test5C3Rank(self):
        n=5
        r=3
        c=self.get5C3()
        self._testRank(n,r,c)

    def test5C3Unrank(self):
        n=5
        r=3
        c=self.get5C3()
        self._testUnrank(n,r,c)

    def testScale(self):
        n=2048
        r=1024
        t0=time.time()
        k=combinations.choose(n,r)//2
        t1=time.time()
        tChoose=t1-t0
        c=combinations.unrank(n,r,k)
        t2=time.time()
        tUnrank=t2-t1
        j=combinations.rank(n,r,c)
        t3=time.time()
        tRank=t3-t2
#        print('choose time=%.3f, unrank time=%.3f, rank time=%.3f' % (tChoose,tUnrank,tRank))
        self.assertLess(tChoose,0.01)
        self.assertLess(tUnrank,0.1)
        self.assertLess(tRank,0.01)
        
        
if __name__ == '__main__':
    unittest.main()
