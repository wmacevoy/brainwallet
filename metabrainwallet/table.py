class Table:    
    def __init__(self,db,name,types):
        self._db = db
        self._name = name
        self._types = types
        # id is first
        columns = list(self._types.keys())
        columns.sort(key = lambda x: x if x != 'id' else '')
        self._columns = columns
        columnsExceptId = columns.copy()
        columnsExceptId.remove('id')        
        self._columnsExceptId = columnsExceptId

    @property
    def db(self):
        return self._db

    @property
    def name(self):
        return self._name

    @property
    def types(self):
        return self._types

    @property
    def columns(self):
        return self._columns

    @property
    def columnsExceptId(self):
        return self._columnsExceptId
    
    def cursor(self):
        return self.db.cursor()

    def execute(self,sql,parameters=None, commit = True):
        return self.db.execute(sql,parameters, commit)

    def createIndex(self,columns,unique=False):
        index=f"index_{self.name}_on_{'__'.join(columns)}"
        sql=f"create {'unique' if unique else ''} index if not exists {index} on {self.name}({','.join(columns)})"
        self.execute(sql=sql,parameters=None,commit=True)

    def dropIndex(self,columns):
        index=f"index_{self.name}_on_{'__'.join(columns)}"
        sql=f"drop index if exists {index}"
        self.execute(sql=sql,parameters=None,commit=True)
        
    def dropTable(self):
        sql = f"drop table {self.name}"
        self.execute(sql=sql,parameters=None,commit=True)
        
    def createTable(self):
        columns = self.columns
        types = self.types
        decls = list(map(lambda column : column + " " + types[column]['dbType'],columns))
        declstr = ",".join(decls)
        sql = f"create table if not exists {self.name} ({declstr})"
        self.execute(sql=sql,parameters=None,commit=True)
        
    def save(self,record, commit = True):
        if record.id != None:
            self.update(record.memo,commit)
        else:
            memo = record.memo
            id = self.insert(memo,commit)
            record.id = id

    def update(self, memo, commit = True):
        if memo == None:
            return
        types = self.types        
        updates =[]
        parameters = []
        columns=self.columnsExceptId
        for column in columns:
            if column in memo:
                updates.append(f"{column} = ?")
                parameters.append(types[column]['db'](memo[column]))
        parameters.append(int(memo['id']))
        updatestr = ",".join(updates)
        sql = f"update {self.name} set {updatestr} where id = ?"
        self.execute(sql,parameters, commit)

    def insert(self,memo, commit = True):
        columns=self.columnsExceptId
        types=self.types
        columnstr = ",".join(columns)
        questions = ",".join("?"*len(columns))
        sql = f"insert into {self.name} ({columnstr}) values ({questions})"
        parameters = list(map(lambda column: types[column]['db'](memo[column]),columns))
        cursor = self.execute(sql,parameters, commit)
        return cursor.lastrowid

    def getIds(self):
        sql = f"select (id) from {self.name}"
        cursor = self.execute(sql)
        rows = cursor.fetchall()
        ids = [None]*len(rows)
        for k in range(len(rows)):
            ids[k] = int(rows[k][0])
        return ids

    def deletebyId(self, id, commit = True):
       sql = f"delete from {self.name} where id = ?"
       parameters = (int(id))
       self.execute(sql, parameters, commit)

    def fullRow2Memo(self,row):
        columns=self.columns
        types=self.types
        memo={}
        for c in range(len(columns)):
            column = columns[c]
            memo[column]=types[column]['py'](row[c])
        return memo
        
    def loadMemoById(self,id):
        columnstr = ",".join(self.columns)
        sql = f"select {columnstr} from {self.name} where id=?"
        parameters = (int(id),)
        cursor=self.execute(sql,parameters)
        rows = cursor.fetchall()
        if len(rows)==0:
            return None
        else:
            row = rows[0]
            memo = self.fullRow2Memo(rows[0])
            return memo

    def loadMemosByColumns(self, wheres):
        whereColumns=list(wheres.keys())
        types=self.types
        columnstr = ",".join(self.columns)
        wherestr = "(" + ") and (".join(map(lambda column : f"{column} = ?",whereColumns)) + ")"
        parameters = list(map(lambda column : types[column]['db'](wheres[column]),whereColumns))
        sql = f"select {columnstr} from {self.name} where {wherestr}"
        cursor = self.execute(sql,parameters)
        rows = cursor.fetchall()
        memos=list(map(lambda row : self.fullRow2Memo(row),rows))
        return memos
        
    def loadById(self, record, id):
        memo = self.loadMemoById(id)
        record.update(memo)
