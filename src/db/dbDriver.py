import sqlite3 as db
import sys
import traceback


class DbDriver:
    conn = None

    def connect(self):
        try:
            self.conn = db.connect("../databases/funBot.db")
        except db.Error:
            print("Error connect to db.")
            traceback.print_exc()
            sys.exit()

    def getById(self, id):
        # if self.conn is None:
        #     return
        try:
            # conn = db.connect("../databases/funBot.db")
            self.conn = db.connect("../databases/funBot.db")
            # cursor = conn.cursor()
            cursor = self.conn.cursor()
            cursor = cursor.execute("select result from mapping where id = ? ", (id,))
            arr = cursor.fetchone()
            print(f'arr={arr}')
            result = None
            if (arr is not None) and (len(arr) != 0):
                result = arr[0]
                print(f'result = {result}')
            # conn.close()
            self.conn.close()
            print(f'result = {result}')
            return result
        except db.Error:
            print(f"Can't execute query for id = {id}")
            traceback.print_exc()
