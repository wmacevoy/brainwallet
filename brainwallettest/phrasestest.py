#!/usr/bin/env python

import inspect
import os
import sys
import unittest

currentdir = os.path.dirname(
    os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)

sys.path.insert(0, parentdir + "/brainwallet")

from rng import RNG
from phrases import Phrases


class PhrasesTest(unittest.TestCase):
    rng = RNG()

    def mkPhrase(self, language, length):
        phrases = Phrases.forLanguage(language)
        words = phrases.words
        phrase = [words[self.rng.next(len(words))] for i in range(length)]
        return phrases.space().join(phrase)

    def testAmbiguity(self):
        languages = Phrases.getLanguages()
        allWords = dict()
        for language in languages:
            phrases = Phrases.forLanguage(language)
            for word in phrases.words:
                if word not in allWords:
                    allWords[word] = dict()
                index = phrases.invWords[word]
                if index not in allWords[word]:
                    allWords[word][index] = set()
                allWords[word][index].add(language)

        ambiguous = False
        for word in allWords:
            indexs = allWords[word]
            if len(indexs) <= 1:
                continue
            ambiguous = True
            for index in indexs:
                for lang in indexs[index]:
                    print ("word %s in %s index %d" % (word, index, lang))

        assert not ambiguous

    def testRankOrdered(self):
        n = 10
        r = 5
        k = 12345
        ordered = True
        c = Phrases.unrank(n,r,k,ordered)
        self.assertEqual(c,[1,2,3,4,5])

    def testRankUnordered(self):
        n = 10
        r = 5
        k = 100
        ordered = False
        c = Phrases.unrank(n,r,k,ordered)
        self.assertEqual(c,[8, 7, 4, 3, 2])
        

    def testUnrankUnordered(self):
        n = 10
        r = 5
        c = [8, 7, 4, 3, 2]
        ordered = False
        k = Phrases.rank(n,r,c,ordered)
        self.assertEqual(k,100)
        
    def _testPhrase(self, language, phrase):
        assert Phrases.forLanguage(language).isPhrase(phrase), \
            "phrase='%s' language=%s" % (phrase, language)
        for ordered in [True,False]:
            if not Phrases.forLanguage(language).isPhrase(phrase,ordered):
                continue
            try:
                number = Phrases.forLanguage(language).toNumber(phrase,ordered)
            except ValueError:
                print ("phrase='%s' language=%s ordered=%r" % (phrase, language, ordered))
                raise

            detects = Phrases.detectLanguages(phrase)
            for lang2 in detects:
                number2 = Phrases.forLanguage(lang2).toNumber(phrase,ordered)
                phrase2 = Phrases.forLanguage(lang2).toPhrase(number,ordered)
                self.assertEqual(number,number2, \
                                "phrase='%s' language=%s" % (phrase, language))
                if not ordered:
                    phrase=Phrases.toList(phrase)
                    phrase.sort()
                    phrase2=Phrases.toList(phrase)
                    phrase2.sort()
                self.assertEqual(phrase,phrase2, \
                             "phrase='%s' language=%s" % (phrase, language))

    def _testPhrases(self, language):
        for number in range(100000):
            phrase = Phrases.forLanguage(language).toPhrase(number)
            self._testPhrase(language, phrase)

        for length in range(1, 20):
            phrase = self.mkPhrase(language, length)
            self._testPhrase(language, phrase)

    def testDecimal(self):
        (decimal,invDecimal) = Phrases.getWords("decimal")
        self.assertEqual(2048,len(decimal))
        for k in range(len(decimal)):
            self.assertEqual(str(k),decimal[k])

    def testPhrase(self):
        languages = Phrases.getLanguages()
        for language in ["english","decimal",
                         "chinese_simplified", "chinese_traditional",
                         "french", "italian", "japanese","korean", "spanish"]:
            assert language in languages
        for language in languages:
            self._testPhrases(language)


if __name__ == '__main__':
    unittest.main()
