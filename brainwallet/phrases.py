import os
import sys
import re
import math
from check import Check

class Phrases:
    _PHRASES=dict()

    @classmethod
    def forLanguage(cls,language):
        if not language in cls._PHRASES:
            cls._PHRASES[language]=Phrases(language)
        return cls._PHRASES[language]

    @classmethod
    def _getDirectory(cls):
        return os.path.join(os.path.dirname(__file__), "wordlist")

    @classmethod
    def getLanguages(cls):
        languages=[]
        suffex=".txt"
        for filename in os.listdir(cls._getDirectory()):
            if filename.endswith(suffix):
                language=Check.toString(filename[:-len(suffex)])
                languages.add(language)
        return languages


    @classmethod
    def _getFilename(cls,language):
        filename = "%s/%s.txt" % (cls._getDirectory(), language)
        return filename

    @classmethod
    def getWords(cls,language):
        filename = cls._getFilename(language)
        if Check.PYTHON3:
            file = open(filename,"r",encoding="utf-8")
        else:
            file = open(filename,"r")
        words = [Check.toString(word).strip() for word in file.readlines()]

        words.sort()

        if len(words)<2: 
            raise ValueError("too few words")
        for i in range(len(words)):
            if len(words[i])==0: 
                raise ValueError("empty word")
            if i > 0 and words[i] == words[i-1]: 
                raise ValueError("duplicate word")
        return words

    @classmethod
    def invertWords(cls,words):
        invWords=dict()
        for i in range(len(words)):
            invWords[words[i]]=i
        return invWords

    def __init__(self, language):
        self.words = self.getWords(language)
        self.invWords = self.invertWords(self.words)
        self.language = language
        self.radix = len(self.words)

    @classmethod
    def detectLanguage(cls, phrase):
        languages = cls.getLanguages()

        for lang in cls.getLanguages():
            phrases = cls.forLanguage(lang)
            if phrases.isPhrase(phrase):
                return lang

        raise ConfigurationError("Language not detected")

    def space(self):
        if self.language == "japanese":
            return u"\u3000"
        else:
            return u" "

    def toList(self,_value):
        value=_value
        if not isinstance(value,list):
            value = re.split(u"[ \u3000]",value,flags=re.UNICODE)
        return value

    def isPhrase(self,words):
        words=self.toList(words)
        for word in words:
            if not word in self.invWords: return False
        return True

    def _offset(self,length): # number of phrases shorter than length
        return ((pow(self.radix,length)-1)//(self.radix-1))-1

    def _length(self,number):
        length=int(math.floor(math.log((number+1)*(self.radix-1)+1,self.radix)))
        while self._offset(length+1) <= number: length += 1
        while self._offset(length)  > number: length += 1
        return length
                          
    def toNumber(self,phrase):
        phrase=self.toList(phrase)
        if not self.isPhrase(phrase):
            raise ValueError("unknown phrase")
        length=len(phrase)
        number = 0
        for i in range(length):
            digit = self.invWords[phrase[i]]
            number = number*self.radix + digit
        number += self._offset(length)
        return number

    def toPhrase(self,number):
        length=self._length(number)
        number -= self._offset(length)
        words = [u""]*length
        for i in range(length):
            words[length-1-i]=self.words[number % self.radix]
            number = number // self.radix
        phrase=self.space().join(words)
        return phrase
        
def test():
    phrases = Phrases("test")
    known = dict()
    for i in xrange(0,100000):
        words=phrases.toPhrase(i)
        number=phrases.toNumber(words)
        assert not words in known, "collision " + str(words)
        assert i == number, "missed " + str(words)
        known[words]=number

def main():
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        test()
        return

    phrases = Phrases("english")
    for i in range(1,len(sys.argv)):
        x=sys.argv[i]

        if x.isdigit():
            y = phrases.toPhrase(int(x))
            print("phrase(" + str(int(x)) + ")=" + str(y))
        else:
            y = phrases.toNumber(x)
            print("number(" + str(x) + ")=" + str(y))

if __name__ == "__main__":
    main()
