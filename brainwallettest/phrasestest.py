#!/usr/bin/env python

import inspect,math,os,sys,unittest

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)

sys.path.insert(0,parentdir+"/brainwallet") 

from rng import RNG
from phrases import Phrases

class PhrasesTest(unittest.TestCase):
    rng=RNG()

    def mkPhrase(self,language,length):
        phrases = Phrases.forLanguage(language)
        words = phrases.words
        phrase = [words[self.rng.next(len(words))] for i in range(length)]
        return phrases.space().join(phrase)

    def testAmbiguity(self):
        languages=Phrases.getLanguages()
        allWords = dict()
        for language in languages:
            phrases = Phrases.forLanguage(language)
            for word in phrases.words:
                if not word in allWords:
                    allWords[word]=dict()
                index = phrases.invWords[word]
                if not index in allWords[word]:
                    allWords[word][index]=set()
                allWords[word][index].add(language)

        ambiguous = False
        for word in allWords:
            indexs = allWords[word]
            if len(indexs)<=1: continue
            ambiguous = True
            for index in indexs:
                for lang in indexs[index]:
                    print ("word %s in %s index %d" % (word,index,lang))
                
        assert not ambiguous

    def _testPhrase(self,language,phrase):
        assert Phrases.forLanguage(language).isPhrase(phrase), "phrase='%s' language=%s" % (phrase, language)
        number = Phrases.forLanguage(language).toNumber(phrase)
        detects = Phrases.detectLanguages(phrase)
        for lang2 in detects:
            number2 = Phrases.forLanguage(lang2).toNumber(phrase)
            phrase2 = Phrases.forLanguage(lang2).toPhrase(number)
            assert number == number2
            assert phrase == phrase2
    
    def _testPhrases(self,language):
        for number in range(100000):
            phrase=Phrases.forLanguage(language).toPhrase(number)
            self._testPhrase(language,phrase)

        for length in range(1,20):
            phrase=self.mkPhrase(language,length)
            self._testPhrase(language,phrase)

    def testPhrase(self):
        languages=Phrases.getLanguages()
        for language in ["chinese_simplified", "chinese_traditional", "english", "french", "italian", "japanese", "korean", "spanish" ]:
            assert language in languages
        for language in languages:
            self._testPhrases(language)

if __name__ == '__main__':
    unittest.main()
