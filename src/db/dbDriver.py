import sqlite3 as db
import sys
import traceback


class DbDriver:

    DB_PATH = None

    def __init__(self, is_mock=False):
        self.DB_PATH = "../databases/funBot.db"
        if not is_mock:
            self.test_connection()

    def test_connection(self):
        try:
            conn = db.connect(self.DB_PATH)
        except db.Error:
            print("Error connect to db.")
            traceback.print_exc()
            sys.exit()
        finally:
            conn.close()

    def getById(self, id):
        try:
            conn = db.connect(self.DB_PATH)
            cursor = conn.cursor()
            cursor = cursor.execute("select result from mapping where id = ? ", (id,))
            arr = cursor.fetchone()
            print(f'arr={arr}')
            result = None
            if (arr is not None) and (len(arr) != 0):
                result = arr[0]
                print(f'result = {result}')
            print(f'result = {result}')
            return result
        except db.Error:
            print(f"Can't execute query for id = {id}")
            traceback.print_exc()
        finally:
            conn.close()

    def getAllowedChats(self):
        try:
            conn = db.connect(self.DB_PATH)
            cursor = conn.cursor()
            cursor = cursor.execute("select * from chats")
            allowed_chats = [item[0] for item in cursor.fetchall()]
            return allowed_chats
        except db.Error:
            print(f"Can't execute query for id = {id}")
            traceback.print_exc()
        finally:
            conn.close()
