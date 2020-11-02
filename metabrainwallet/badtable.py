from table import Table
from bad import Bad

class BadTable(Table):
    def __init__(self,db):
        super().__init__(db,Bad.TABLE,Bad.TYPES)

    def save(self,bad, commit = True):
        id = bad.id
        word = bad.word
        if id == None and word != None:
            sql=f"select id from bad where word = ?"
            parameters=(word,)
            cursor=self.execute(sql,parameters)
            rows = cursor.fetchall()
            if len(rows) > 0:
                bad.id = rows[0][0]
        super().save(bad, commit)

    def createTable(self):
        super().createTable()
        self.createIndex(columns=['word'],unique=True)

    def dropTable(self):
        self.dropIndex(columns=['word'])
        super().dropTable()
        
    def addAll(self,words):
        for word in words:
            word = Bad.computeHash(word)
            memos = self.loadMemosByColumns({'word':word})
            if len(memos) == 0:
                bad = Bad({'word':word})
                self.save(bad)
                
    def addBadWords(self):
        words=Bad.getBadWords()
        self.addAll(words)

    def contains(self,word):
        word = Bad.computeHash(word)
        memos = self.loadMemosByColumns({'word':word})
        return len(memos)>0
