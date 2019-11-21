from memoable import Memoable

class Translation(Memoable):
    TABLE="translation"
    TYPES={
        'id' : {
            'dbType' : 'integer primary key',
            'db'  : lambda value : int(value),
            'py'  : lambda value : int(value) if value != None else None,
            'default': None
        },
        'originalId' : {
            'dbType' : 'integer not null',
            'db'  : lambda value : int(value),
            'py'  : lambda value : int(value) if value != None else None,
            'default': None
        },
        'translatedId' : {
            'dbType' : 'integer not null',
            'db'  : lambda value : int(value),
            'py'  : lambda value : int(value) if value != None else None,
            'default': None
        }
    }

    def __init__(self,memo={}):
        super().__init__(Translation.TYPES,memo)

    def orignal(self,db):
        if self.originalId == None:
            return None
        phrase=Phrase()
        db.phrase.loadById(phrase,self.originalId)
        return phrase

    def translated(self,db):
        if self.translatedId == None:
            return None
        phrase=Phrase()
        db.phrase.loadById(phrase,self.translatedId)
        return phrase
