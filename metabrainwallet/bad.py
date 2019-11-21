import sys,os,re,zlib
from memoable import Memoable
from hash import Hash

class Bad(Memoable):
    TABLE="bad"
    TYPES={
        'id' : {
            'dbType' : 'integer primary key',
            'db'  : lambda value : int(value),
            'py'  : lambda value : int(value) if value != None else None,
            'default': None
        },
        'word' : {
            'dbType' : 'text not null',
            'db'  : lambda value : str(value),
            'py'  : lambda value : str(value) if value != None else None,
            'default': None
        }
    }

    @classmethod
    def isHashed(cls,word):
        return word == None or word.startswith("#")

    @classmethod
    def computeHash(cls,word):
        if cls.isHashed(word):
            return word
        state=Hash.hashString(word)
        statestr=format(state, '012x')
        return f"#{statestr}"

    @classmethod        
    def equality(cls,word1,word2):
        word1=str(word1)
        word2=str(word2)
        h1=cls.isHashed(word1)
        h2=cls.isHashed(word2)
        return (h1 == h2 and word1 == word2) or (cls.computeHash(word1) == cls.computeHash(word2))

    @property
    def hashed(self):
        return Bad.isHashed(self.word)

    def hash(self):
        self.word=Bad.computeHash(self.word)

    def equals(self,to):
        return self.equality(self.word,to.word)

    # https://www.cs.cmu.edu/~biglou/resources/bad-words.txt
    @classmethod
    def getBadWords(cls):
        dir = os.path.dirname(os.path.realpath(__file__))
        filename=dir + '/bad-words.txt'
        file = open(filename,"r",encoding="utf-8")
        badWords = set()
        for wordCount in file.readlines():
            line = re.split(u"[ \u3000\r\n\t]+",wordCount,flags=re.UNICODE)
            word = line[0].lower()
            if len(word) > 0:
                badWords.add(word)
        file.close()
        return badWords

    def __init__(self,memo={}):
        super().__init__(Bad.TYPES,memo)
