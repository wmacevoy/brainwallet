#!/usr/bin/env python

import inspect,math,os,sys,unittest

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)

sys.path.insert(0,parentdir+"/brainwallet") 

import cStringIO

from brainwallet import BrainWallet

class BrainWalletTest(unittest.TestCase):
    debug = 0
    def __init__(self, *args, **kwargs):
        super(BrainWalletTest, self).__init__(*args, **kwargs)
        self.outs=[]
        self.cases = 1

    def setCase(self,k):
        if k == 0:
            self.secret = "always traffic bacon first crystal pistol sadness state visa misery degree nature fork glow mango"
            self.master = "xprv9s21ZrQH143K4F1FoccpGyVV4mh5SRZcejV4cKfXKX6jDJvpowK63fWtssVBpKS3ktt4WuvohqqjcMScrcYbyY4V5zV84y1cXzPgCJkF362"

    

    def begin(self): # capture output
        self.outs.append(sys.stdout)
        sys.stdout = cStringIO.StringIO()

    def end(self): # return captured output
        strval = sys.stdout.getvalue()
        sys.stdout = self.outs.pop()
        return strval

    def _testMasterFromSecretCli(self,k):
        # https://github.com/wmacevoy/brainwallet/issues/12
        self.setCase(k)
        brainWallet = BrainWallet()
        args = ["--secret="+self.secret,"--master"]
        self.begin()
        brainWallet.cli(args)
        master1=self.end()
        self.begin()
        print self.master
        master2=self.end()
        assert master1 == master2

    def testMasterFromSecretCli(self):
        for k in range(self.cases):
            self._testMasterFromSecretCli(k)

    def _testMasterFromSecretObj(self,k):
        # https://github.com/wmacevoy/brainwallet/issues/12
        self.setCase(k)
        brainWallet = BrainWallet()
        brainWallet.setSecret(self.secret)
        seed = brainWallet.getSeed()
        result = brainWallet.getHDMasterKey(seed)
        assert self.master == result

    def testMasterFromSecretObj(self):
        for k in range(self.cases):
            self._testMasterFromSecretObj(k)

if __name__ == '__main__':
    unittest.main()
