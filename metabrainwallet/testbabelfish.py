#!/usr/bin/env python3

from unittest import TestCase, main
from babelfish import Babelfish
from languages import LANGUAGES_GOOGLE

class TestBabelfish(TestCase):
    def testMissingLanguage(self):
        language="Not A Language"
        babelfish = Babelfish()
        self.assertRaises(KeyError, lambda: babelfish.addLanguage(language))

    def testHelloWorld(self):
        phrase="hello world"
        babelfish = Babelfish()
        for language in LANGUAGES_GOOGLE:
            babelfish.clearLanguages()
            babelfish.addLanguage(language)
            response=babelfish.translate(phrase)
            self.assertTrue(response != None)
            self.assertTrue(response != "")
            print(response)

if __name__ == '__main__':
    main()
