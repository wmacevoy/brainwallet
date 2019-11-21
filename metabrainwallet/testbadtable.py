#!/usr/bin/env python3

from unittest import TestCase, main
from bad import Bad
from db import Db

class TestBadTable(TestCase):
    def testBadWords(self):
        db=Db()
        db.dbFile="testmetabrainwallet.db"
        db.bad.dropTable()
        db.bad.createTable()
        db.bad.addBadWords()

        self.assertTrue(db.bad.contains('ass'))
        self.assertFalse(db.bad.contains('ok'))
        self.assertFalse(db.bad.contains(''))        

        db.close()

if __name__ == '__main__':
    main()
