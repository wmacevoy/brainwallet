#!/usr/bin/env python

import os,sys
from google.cloud import translate_v2
from languages import LANGUAGES_100M, LANGUAGES_GOOGLE
from dotenv import load_dotenv, find_dotenv

class Babelfish:
    def addCommonLanguages(self):
        for language in LANGUAGES_100M:
            self.addLanguage(language)

    def __init__(self,source='en'):
        if os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')==None:
            load_dotenv(find_dotenv())
        self._source = source
        self._languages = set()
        self._client = None
        self.addCommonLanguages()

    def addLanguage(self,language):
        self._languages.add(LANGUAGES_GOOGLE[language])

    def removeLanguage(self,language):
        self._languages.remove(LANGUAGES_GOOGLE[language])

    def clearLanguages(self):
        self._languages.clear()
    @property
    def source(self):
        return self._source

    @property
    def client(self):
        if self._client == None:
            self._client = translate_v2.Client()
        return self._client

    def translate(self,phrase):
        translations={}
        print(repr(self._languages))
        for target in self._languages:
            if target == self.source:
                translation=phrase
            else:
                response=self.client.translate(phrase, target, None, self.source)
                translation=response['translatedText']
            translations[target]=translation
        return translations
    
def babelfish(*words):
    babelfish = Babelfish()
    for word in words:
        print(repr(babelfish.translate(word)))

def testBabelfish():
    babelfish("pidgin")

def main():
    args = sys.argv
    args.pop(0)
    if len(args) == 0:
        testBabelfish()
    else:
        babelfish(*args)

if __name__ == '__main__':
    main()
