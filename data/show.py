#!/usr/bin/env python3
import os
import sys
import pydblite

class showDB:

    def __init__(self):
        dbDir = os.path.join(os.getcwd(), 'data.db')
        self.db = self.open_db(dbDir)
        self.show_data()

    def open_db(self, dbDir):
        db = pydblite.Base(dbDir)
        if db.exists():
            db.open()
        return db

    def show_data(self):
        for data in self.db:
            print(data)
            print('\n')

if __name__ == '__main__':
    showDB()
