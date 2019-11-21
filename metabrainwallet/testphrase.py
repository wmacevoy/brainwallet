#!/usr/bin/env python3

from unittest import TestCase, main
from phrase import Phrase
from bad import Bad

class TestPhrase(TestCase):
    def testDefaults(self):
        phrase=Phrase()
        self.assertEqual(phrase.id,None)
        self.assertEqual(phrase.language,None)
        self.assertEqual(phrase.content,None)
        self.assertEqual(phrase.frequency,None)

    def contains(self,phrases,word):
        for phrase in phrases:
            if phrase.content == word:
                return True
        return False

    def testCommon(self):
        common=Phrase.getCommon()
        self.assertTrue(self.contains(common,'information'))
        self.assertFalse(self.contains(common,'supercalifragilisticexpialidocious'))
        self.assertFalse(self.contains(common,''))

        
if __name__ == '__main__':
    main()
