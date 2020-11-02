#!/usr/bin/env python

import inspect,math,os,sys,unittest

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)

sys.path.insert(0,parentdir+"/brainwallet") 

from combinations import Combinations

class CombinationsTest(unittest.TestCase):
    def _testCombinations(self,n,r,c):
        nCr=Combinations.choose(n,r)
        self.assertEqual(nCr,len(c))
        for k in range(nCr):
            d = Combinations.get(n,r,k)
            j = Combinations.index(n,r,c[k])
            self.assertEqual(k,j)
            self.assertEqual(len(d),len(c[k]))
            for i in range(r):
                self.assertEqual(d[i],c[k][i])
    def test5C2(self):
        n=5
        r=2
        c=[[0,1],[0,2],[0,3],[0,4],[1,2],[1,3],[1,4],[2,3],[2,4],[3,4]]        
        self._testCombinations(n,r,c)

    def test5C3(self):
        n=5
        r=3
        c=[[0,1,2],[0,1,3],[0,1,4],[0,2,3],[0,2,4],[0,3,4],[1,2,3],[1,2,4],[1,3,4],[2,3,4]]
        self._testCombinations(n,r,c)

if __name__ == '__main__':
    unittest.main()
