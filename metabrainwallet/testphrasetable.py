#!/usr/bin/env python3

from unittest import TestCase, main
from phrase import Phrase
from db import Db

class TestPhraseTable(TestCase):
    def testCommon(self):
        db=Db()
        db.dbFile="testmetabrainwallet.db"
        db.phrase.dropTable()
        db.phrase.createTable()
        db.phrase.addCommon('count_1w100.txt')

        good = Phrase({'language':'en', 'content': 'information'})
        bad = Phrase({'language':'en', 'content': 'supercalifragilisticexpialidocious'})
        empty = Phrase({'language':'en', 'content': ''})
        self.assertTrue(db.phrase.contains(good))
        self.assertFalse(db.phrase.contains(bad))
        self.assertFalse(db.phrase.contains(empty))

        db.close()

if __name__ == '__main__':
    main()
