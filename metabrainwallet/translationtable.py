from table import Table
from phrase import Phrase
from translation import Translation

class TranslationTable(Table):
    def __init__(self,db):
        super().__init__(db,Translation.TABLE,Translation.TYPES)
    def translations(self,phrase,language):
        db.phrase.save(phrase)
        
        if phrase.id == None:
            phraseMemos = self.db.phrase.loadMemosByColumns({'language':phrase.language,'content':phrase.content})
            phrase.update(
        memos=self.loadMemosByColumns({
        
