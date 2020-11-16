#!/usr/bin/env python

import inspect
import os
import sys
import unittest

currentdir = os.path.dirname(
    os.path.abspath(inspect.getfile(inspect.currentframe())))

parentdir = os.path.dirname(currentdir)

sys.path.insert(0, parentdir + "/brainwallet")

from brainwallet import BrainWallet
from millerrabin import MillerRabin
from check import Check
from phrases import Phrases
import combinations

if Check.PYTHON3:
    import io
else:
    import cStringIO


class BrainWalletTest(unittest.TestCase):
    debug = 0

    def __init__(self, *args, **kwargs):
        super(BrainWalletTest, self).__init__(*args, **kwargs)
        self.outs = []
        self.cases = 1

    def setCase(self, k):
        if k == 0:
            self.secret = (
                "always traffic bacon first crystal pistol "
                "sadness state visa misery degree nature fork glow mango"
            )
            self.master = (
                "xprv9s21ZrQH143K4F1FoccpGyVV4mh5SRZcejV4cKfXKX6jDJvpowK63fWt"
                "ssVBpKS3ktt4WuvohqqjcMScrcYbyY4V5zV84y1cXzPgCJkF362"
            )

    def begin(self):  # capture output
        self.outs.append(sys.stdout)
        if Check.PYTHON3:
            sys.stdout = io.StringIO()
        else:
            sys.stdout = cStringIO.StringIO()

    def end(self):  # return captured output
        strval = sys.stdout.getvalue()
        sys.stdout = self.outs.pop()
        return strval

    def _testMasterFromSecretCli(self, k):
        # https://github.com/wmacevoy/brainwallet/issues/12
        self.setCase(k)
        brainWallet = BrainWallet()
        args = ["--secret=" + self.secret, "--master"]
        self.begin()
        brainWallet.cli(args)
        master1 = self.end()
        self.begin()
        print (self.master)
        master2 = self.end()
        assert master1 == master2

    def testMasterFromSecretCli(self):
        for k in range(self.cases):
            self._testMasterFromSecretCli(k)

    def _testMasterFromSecretObj(self, k):
        # https://github.com/wmacevoy/brainwallet/issues/12
        self.setCase(k)
        brainWallet = BrainWallet()
        brainWallet.setSecret(self.secret)
        seed = brainWallet.getSeed()
        result = brainWallet.getHDMasterKey(seed)
        assert self.master == result

    def testMaxLengthFixedOrder(self):
        brainWallet = BrainWallet()
        mr = MillerRabin()
        brainWallet.setOrderMatters(True)        
        brainWallet.setMaxLength(10)
        number = 0
        for k in range(1,10+1):
            number += 2048**k
        prime = mr.prevPrime(number)            
        self.assertEqual(prime,brainWallet.getPrime())
        self.assertEqual(10,brainWallet.getMaxLength())


    def testMaxLengthAnyOrder(self):
        brainWallet = BrainWallet()
        mr = MillerRabin()

        brainWallet.setOrderMatters(False)
        brainWallet.setMaxLength(10)
        number = 0
        for k in range(1,10+1):
            number += combinations.choose(2048,k)
        prime = mr.prevPrime(number)
        self.assertEqual(prime,brainWallet.getPrime())
        self.assertEqual(10,brainWallet.getMaxLength())

    def _testRecoverFrom3of5KeysIn(self,bits,language,ordered):
        brainWallet = BrainWallet()
        minimum=3
        shares=5
        brainWallet.cli(["--order-matters=" + str(ordered),"--language=" + language,"--bits=" + str(bits),"--minimum=" + str(minimum),"--shares=" + str(shares),"--randomize"])
        keys=[""]*6
        self.begin()
        brainWallet.cli(["--secret"])
        secret1 = self.end().rstrip()
        keys[0]=secret1

        for i in range(1,6):
            self.begin()
            brainWallet.cli(["--key" + str(i)])
            keys[i] = self.end().rstrip()
            
        for i1 in range(1,6):
            for i2 in range(1,6):
                for i3 in range(1,6):
                    for i4 in range(0,6):
                        if i1 == i2 or i1 == i3 or i1 == i4: continue
                        if i2 == i3 or i2 == i4: continue
                        if i3 == i4: continue
                        brainWallet2 = BrainWallet()

                        args=["--order-matters=" + str(ordered),"--language=" + language,"--bits=" + str(bits)]
                        args.append("--key"+str(i1)+"="+keys[i1])
                        args.append("--key"+str(i2)+"="+keys[i2])
                        args.append("--key"+str(i3)+"="+keys[i3])
                        if i4 != 0:
                            args.append("--key"+str(i4)+"="+keys[i4])
                        args.append("--secret")
                        self.begin()                    
                        brainWallet2.cli(args)
                        secret2 = self.end().rstrip()
                        self.assertEqual(secret1,secret2)

    def testRecoverFrom3of5Keys(self):
        bits=160
        for language in Phrases.getLanguages():
            for ordered in [True, False]:
                self._testRecoverFrom3of5KeysIn(bits,language,ordered)
        

    def testMasterFromSecretObj(self):
        for k in range(self.cases):
            self._testMasterFromSecretObj(k)


if __name__ == '__main__':
    unittest.main()
