import os
import sys
import re
import math
from check import Check
import combinations

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

    _LANGUAGES=None
    @classmethod
    def getLanguages(cls):
        if cls._LANGUAGES == None:
            languages=[]
            suffix=".txt"
            for filename in os.listdir(cls._getDirectory()):
                if filename.endswith(suffix):
                    language=Check.toString(filename[:-len(suffix)])
                    languages.append(language)
            cls._LANGUAGES=languages
        return cls._LANGUAGES

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

        words = []
        for word in file.readlines():
            word=Check.toString(word)
            comment = word.rfind("#")
            if comment >= 0:
                word=word[0:comment]
            words.extend(cls.toList(word))

        file.close()

        invWords = dict()
        for i in range(len(words)):
            if words[i] in invWords:
                raise ValueError("duplicate word " + words[i])
            invWords[words[i]]=i

        if len(words)<2: 
            raise ValueError("too few words")
        return (words,invWords)

    def __init__(self, language):
        self.language = language
        (self.words,self.invWords) = self.getWords(language)
        self.radix = len(self.words)

    @classmethod
    def detectLanguages(cls, phrase):
        detect=set()
        languages = cls.getLanguages()

        for lang in cls.getLanguages():
            phrases = cls.forLanguage(lang)
            if phrases.isPhrase(phrase):
                detect.add(lang)
        return detect

    def detectLanguage(cls, phrase):
        detect = cls.detectLanguages(phrase)
        if len(detect)==1:
            return detect.pop()
        raise ConfigurationError("Language not detected")

    def space(self):
        if self.language == "japanese":
            return u"\u3000"
        else:
            return u" "

    @classmethod
    def toList(cls,_value):
        value=_value
        if not isinstance(value,list):
            value = re.split(u"[ \u3000\r\n\t]+",value,flags=re.UNICODE)
        else:
            value=value[:] # copy

        while len(value)>0 and len(value[len(value)-1])==0: 
            del value[len(value)-1]

        while len(value)>0 and len(value[0])==0:
            del value[0]

        return value

    def isPhrase(self,words, orderMatters = True):
        words=self.toList(words)
        wordSet=set() if not orderMatters else None
        for word in words:
            if not word in self.invWords: return False
            if not orderMatters:
                if word in wordSet:
                    return False
                else:
                    wordSet.add(word)
        
        return True

    @classmethod
    def count(cls,n,r,orderMatters):
        if n < 2:
            raise ValueError("invalid parameters")
        if orderMatters:
            count = n**r if r > 0 else 0
        else:
            count = combinations.choose(n,r) if r > 0 else 0
        return count

    @classmethod    
    def offset(cls,n,r,orderMatters):
        if n < 2 or r <= 0:
            raise ValueError("invalid parameters")
        offset = 0
        for k in range(1,r):
            count = cls.count(n,k,orderMatters)
            if count == 0:
                raise ValueError("invalid parameters")
            offset += count
        return offset

    @classmethod
    def rank(cls,n,r,c,orderMatters):
        if orderMatters:
            if n < 2 or len(c) != r:
                raise ValueError("invalid parameters")
            for i in range(r):
                if c[i] < 0 or n <= c[i]:
                    raise ValueError("invalid parameters")
            a = 0
            for i in range(r):
                a = a*n + c[i]
            return a
        else:
            return combinations.rank(n,r,c)

    @classmethod
    def unrank(cls,n,r,k,orderMatters):
        if orderMatters:
            if n < 2 or r < 0 or k < 0 or k >= n**r:
                raise ValueError("invalid parameters")
            a = k
            c = [0]*r
            for i in range(r):
                (a,c[r-i-1]) = divmod(a,n)
            return c
        else:
            return combinations.unrank(n,r,k)

    def lengthAndOffset(self,number,orderMatters):
        length = 1
        offset = 0
        while True:
            count = self.count(self.radix,length,orderMatters)
            if count == 0:
                return (None,offset)
            if number < offset+count: break
            offset += count
            length += 1
        return (length,offset)

    def toNumber(self,phrase,orderMatters=True):
        phrase=self.toList(phrase)
        if not self.isPhrase(phrase,orderMatters):
            raise ValueError("unknown phrase")
        length = len(phrase)
        c = [self.invWords[phrase[i]] for i in range(length)]
        return self.offset(self.radix,length,orderMatters)+self.rank(self.radix,length,c,orderMatters)

    def toPhrase(self,number,orderMatters=True):
        (length,offset)=self.lengthAndOffset(number,orderMatters)
        if length == None:
            raise ValueError("unrepresentable")
        c = self.unrank(self.radix,length,number - offset,orderMatters)
        words = [self.words[c[i]] for i in range(length)]
        if not orderMatters:
            words.sort()
        phrase=self.space().join(words)
        return phrase

    def toNumber0(self,phrase):
        phrase=self.toList(phrase)
        if not self.isPhrase(phrase):
            raise ValueError("unknown phrase")
        length=len(phrase)
        number = 0
        for i in range(length):
            digit = self.invWords[phrase[i]]
            number = number*self.radix + digit
        number += self.offset(length)
        return number

    def toPhrase0(self,number):
        length=self._length(number)
        number -= self.offset(length)
        words = [u""]*length
        for i in range(length):
            words[length-1-i]=self.words[number % self.radix]
            number = number // self.radix
        phrase=self.space().join(words)
        return phrase
    
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
