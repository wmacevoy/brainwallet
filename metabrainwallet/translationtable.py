from table import Table
from phrase import Phrase
from translation import Translation
from babelfish import Babelfish

class TranslationTable(Table):
    def __init__(self,db):
        super().__init__(db,Translation.TABLE,Translation.TYPES)
        self._babelfish = None

    def createTable(self):
        super().createTable()
        self.createIndex(columns=['originalId','translatedId'],unique=True)

    def dropTable(self):
        self.dropIndex(columns=['originalId','translatedId'])
        super().dropTable()
    @property
    def babelfish(self):
        if self._babelfish == None:
            babelfish = Bablefish()
        return babelfish
    def find(self,original,language):
        self.db.phrase.save(original)
        sql="select translated.id from translation join phrase original on translation.originalId = original.id join phrase translated on translation.translatedId = translated.id where original.language = ? and original.content = ? and translated.language = ?"
        parameters=(original.language,original.content,language)
        cursor = self.execute(sql,parameters)
        rows = cursor.fetchall()
        ans=[]
        for row in rows:
            id=row[0]
            translated = Phrase()
            self.db.phrase.loadById(translated,id)
            ans.append(translated)
        return ans

    def addTranslation(self,original,translated):
        self.db.phrase.save(original)
        self.db.phrase.save(translated)
        translation = Translation({'originalId': original.id, 'translatedId':translated.id})
        self.save(translation)
        return translation

    def save(self,translation):
        sql="select id from translation where originalId = ? and translatedId = ?"
        parameters=(translation.originalId,translation.translatedId)
        cursor = self.execute(sql,parameters)
        rows = cursor.fetchall()
        if len(rows) == 0:
            translation.id = self.insert(translation.memo)
        else:
            translation.id = rows[0][0]
        
