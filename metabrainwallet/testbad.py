#!/usr/bin/env python3

from unittest import TestCase, main
from bad import Bad

class TestBad(TestCase):
    def testDefaults(self):
        bad=Bad()
        self.assertEqual(bad.id,None)
        self.assertEqual(bad.word,None)

    def testIdProperty(self):
        bad=Bad()
        bad.id = 21
        self.assertEqual(bad.id,21)
        self.assertEqual(bad.memo['id'],21)

    def testIdMemo(self):
        bad=Bad()
        bad.update({'id':21})
        self.assertEqual(bad.id,21)
        self.assertEqual(bad.memo['id'],21)
        
    def testWordProperty(self):
        bad=Bad()
        bad.word='#@$!'
        self.assertEqual(bad.word,'#@$!')
        self.assertEqual(bad.memo['word'],'#@$!')        

    def testWordMemo(self):
        bad=Bad()
        bad.update({'word':'#@$!'})
        self.assertEqual(bad.word,'#@$!')
        self.assertEqual(bad.memo['word'],'#@$!')

    def testHashEquiv(self):
        bad1=Bad({'word':'x'})
        bad2=Bad({'word':'x'})
        bad3=Bad({'word':'y'})
        self.assertTrue(bad1.equals(bad2))
        self.assertFalse(bad1.equals(bad3))
        bad2.hash()
        bad3.hash()
        self.assertTrue(bad1.equals(bad2))
        self.assertFalse(bad1.equals(bad3))        
        
    def testBadWords(self):
        badWords=Bad.getBadWords()
        self.assertTrue('ass' in badWords)
        self.assertFalse('' in badWords)
        self.assertFalse('ok' in badWords)

if __name__ == '__main__':
    main()
