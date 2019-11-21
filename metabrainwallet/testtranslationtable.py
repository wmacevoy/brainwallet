#!/usr/bin/env python3

from unittest import TestCase, main
from translation import Translation
from phrase import Phrase
from db import Db

class TestTranslationTable(TestCase):
    def testSaveTranslation(self):
        db=Db()
        db.dbFile="testmetabrainwallet.db"
        db.translation.dropTable()
        db.translation.createTable()

        hello = Phrase({'language':'en','content':'hello'})
        hola = Phrase({'language':'es','content':'hola'})

        db.phrase.save(hello)
        db.phrase.save(hola)

        translation = Translation({'originalId':hello.id, 'translatedId':hola.id})
        db.translation.save(translation)

        phrases = db.translation.find(hello,'es')

        self.assertTrue(len(phrases)==1)
        self.assertTrue(phrases[0].id == hola.id)

        db.close()

if __name__ == '__main__':
    main()
