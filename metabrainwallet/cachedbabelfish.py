#!/usr/bin/env python
import sys
from babelfish import Babelfish
from phrase import Phrase
from db import Db

class CachedBabelfish(Babelfish):
    def __init__(self,source='en'):
        super().__init__(source)
        self._db = Db()

    @property
    def db(self):
        return self._db

    def close(self):
        self.db.close()

    def translate(self,phrase):
        translations={}
        for target in self._languages:
            if target == self.source:
                translation=phrase
            else:
                original=Phrase({'language': self.source,'content':phrase})
                self.db.phrase.save(original)
                translateds=self.db.translation.find(original,target)
                if len(translateds)>0:
                    translation=translateds[0].content
                    print(f"{self.source}/{phrase} => {target}/{translation} cached")
                else:
                    response=self.client.translate(phrase, target, None, self.source)
                    translation=response['translatedText']
                    translated = Phrase({'language':target, 'content': translation})
                    self.db.translation.addTranslation(original,translated)
            translations[target]=translation
        return translations
    
def cachedbabelfish(*words):
    cachedBabelfish = CachedBabelfish()
    for word in words:
        print(repr(cachedBabelfish.translate(word)))
    cachedBabelfish.close()

def testcachedbabelfish():
    cachedbabelfish("pidgin")

def main():
    args = sys.argv
    args.pop(0)
    if len(args) == 0:
        testcachedbabelfish()
    else:
        cachedbabelfish(*args)

if __name__ == '__main__':
    main()
