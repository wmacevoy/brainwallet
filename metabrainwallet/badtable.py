from table import Table
from bad import Bad

class BadTable(Table):
    def __init__(self,db):
        super().__init__(db,Bad.TABLE,Bad.TYPES)

    def save(self,bad):
        types = self.types
        id = bad.id
        word = bad.word
        if id == None and word != None:
            sql=f"select id from bad where word = ?"
            parameters=(word,)
            cursor=self.execute(sql,parameters)
            rows = cursor.fetchall()
            if len(rows) > 0:
                bad.id = rows[0][0]
        super().save(bad)

    def createTable(self):
        super().createTable()
        self.execute(f"create unique index if not exists index_{self.name}_word ON {self.name}(word)")

    def dropTable(self):
        self.execute(f"drop index if exists index_{self.name}_word")
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
