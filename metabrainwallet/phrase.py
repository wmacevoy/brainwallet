import sys,os,re
from memoable import Memoable

class Phrase(Memoable):
    TABLE="phrase"
    TYPES={
        'id' : {
            'dbType' : 'integer primary key',
            'db' : lambda value : int(value),
            'py' : lambda value : int(value) if value != None else None,
            'default' : None
        },
        'language' : {
            'dbType' : 'text not null',
            'db' : lambda value : str(value),
            'py' : lambda value : str(value) if value != None else None,
            'default' : None
        },
        'content' : {
            'dbType' : 'text not null',
            'db' : lambda value : str(value),
            'py' : lambda value : str(value) if value != None else None,
            'default' : None
        },
        'frequency' : {
            'dbType' : 'integer',
            'db' : lambda value : int(value) if value != None else None,
            'py' : lambda value : int(value) if value != None else None,
            'default' : None
        }
    }
    
    @classmethod
    def getCommon(cls,filename='count_1w100k.txt'):
        dir = os.path.dirname(os.path.realpath(__file__))        
        filename=dir + '/' + filename
        file = open(filename,"r",encoding="utf-8")
        phrases = list()
        count=0
        for wordCount in file.readlines():
            line = re.split(u"[ \u3000\r\n\t]+",wordCount,flags=re.UNICODE)
            memo = { 'language': 'en', 'content': line[0].lower(), 'frequency': int(line[1]) }
            if len(memo['content']) > 0:
                phrase=Phrase(memo)
                phrases.append(phrase)
        file.close()
        return phrases
    
    def __init__(self,memo={}):
        super().__init__(Phrase.TYPES,memo)
