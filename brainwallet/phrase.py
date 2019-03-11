import os
import sys
import unicodedata

class Phrase:
    _PHRASE=dict()

    @classmethod
    def forLanguage(cls,language):
        if not language in cls._PHRASE:
            cls._PHRASE[language]=Phrase(language)
        return cls._PHRASE[language]

    def __init__(self, language):
        if sys.version < "3":
            with open("%s/%s.txt" % (self._getDirectory(), language), "r") as f:
                self.words = [w.strip().decode("utf8") for w in f.readlines()]
        else:
            with open(
                "%s/%s.txt" % (self._getDirectory(), language), "r", encoding="utf-8"
            ) as f:
                self.words = [w.strip() for w in f.readlines()]
        self.words.sort()
        self.numbers=dict()
        for i in range(len(self.words)):
            self.numbers[self.words[i]]=i
        self.language = language
        self.radix = len(self.words)

    @classmethod
    def _getDirectory(cls):
        return os.path.join(os.path.dirname(__file__), "wordlist")

    @classmethod
    def getLanguages(cls):
        return [
            f.split(".")[0]
            for f in os.listdir(cls._getDirectory())
            if f.endswith(".txt")
        ]

    @classmethod
    def normalizeString(cls, txt):
        if isinstance(txt, str if sys.version < "3" else bytes):
            utxt = txt.decode("utf8")
        elif isinstance(txt, unicode if sys.version < "3" else str):  # noqa: F821
            utxt = txt
        else:
            raise TypeError("String value expected")

        return unicodedata.normalize("NFKD", utxt)

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
            return " "

    _STRING_TYPE=str if sys.version_info[0] >= 3 else basestring
    @classmethod
    def isString(cls,value):
        return isinstance(value,cls._STRING_TYPE)

    def toList(self,phrase):
        result=phrase
        if self.isString(phrase):
            result = self.normalizeString(result)
            result=result.split(" ")
            if self.language == "japanese":
                jResult=[]
                for word in result:
                    jResult.extend(word.split(u"\u3000"))
                result=jResult
        return result

    def toString(self,phrase):
        if not self.isString(phrase):
            phrase = self.space().join(phrase)
        return phrase

    def isPhrase(self,words):
        words=self.toList(words)

        for word in words:
            if not word in self.numbers: return False
        return True

    def toNumber(self,phrase):
        phrase=self.toList(phrase)
        if not self.isPhrase(phrase):
            raise ValueError("unknown phrase")
        c=0
        k=0
        B=self.radix
        for i in range(len(phrase)):
            d = self.numbers[phrase[i]]
            k+=1
            c = c*B+d

        return c+((pow(B,k)-1)//(B-1))-1

    def toPhrase(self,number):
        k = 0;
        B = self.radix
        column = number+1
        while True:
            k+=1
            offset = ((pow(B,k+1)-1)//(B-1));
            if column < offset: break

        offset = ((pow(B,k)-1)//(B-1))
        column -= offset;
        phrase=[self.words[0] for i in range(k)]

        for i in range(k):
            d = column%B
            column=column//B
            phrase[k-1-i]=self.words[d]

        return self.toString(phrase)

def test():
    phrase = Phrase("test")
    phrases = dict()
    for i in xrange(0,10000):
        words=phrase.toPhrase(i)
        number=phrase.toNumber(words)
        assert not words in phrases, "collision " + str(words)
        assert i == number, "missed " + str(words)
        phrases[words]=number

def main():
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        test()
        return

    phrase = Phrase("english")
    for i in range(1,len(sys.argv)):
        x=sys.argv[i]

        if x.isdigit():
            y = phrase.toPhrase(int(x))
            print("phrase(" + str(int(x)) + ")=" + str(y))
        else:
            y = phrase.toNumber(x)
            print("number(" + str(x) + ")=" + str(y))

if __name__ == "__main__":
    main()
