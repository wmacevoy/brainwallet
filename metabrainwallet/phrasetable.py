from table import Table
from phrase import Phrase

class PhraseTable(Table):
    def __init__(self,db):
        super().__init__(db,Phrase.TABLE,Phrase.TYPES)

    def save(self,phrase, commit = True):
        id = phrase.id
        language = phrase.language
        content = phrase.content
        if id == None and language != None and content != None:
            sql=f"select id from phrase where language = ? and content = ?"
            parameters=(language,content)
            cursor=self.execute(sql,parameters)
            rows = cursor.fetchall()
            if len(rows) > 0:
                phrase.id = rows[0][0]
        super().save(phrase,commit)

    def createTable(self):
        super().createTable()
        self.execute(f"create unique index if not exists index_{self.name}_language_content ON {self.name}(language,content)")

    def dropTable(self):
        self.execute(f"drop index if exists index_{self.name}_language_content")
        super().dropTable()

    def addAll(self,phrases):
        for phrase in phrases:
            self.save(phrase)
                
    def addCommon(self,filename='count_1w100k.txt'):
        phrases=Phrase.getCommon(filename)
        self.addAll(phrases)

    def contains(self,phrase):
        memos = self.loadMemosByColumns({'language':phrase.language,'content':phrase.content})
        return len(memos)>0
