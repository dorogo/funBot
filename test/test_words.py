import unittest
from mock import patch
# import src.main
# import src.db.dbDriver as db
from src.db.dbDriver import DbDriver


# https://www.reddit.com/r/learnpython/comments/95x8tr/mocking_fetchone_from_sqlite3/
# https://github.com/AndyLPK247/python-testing-101

class MyTestCase(unittest.TestCase):

    @patch('src.db.dbDriver.DbDriver.getById')
    # @mock.patch.object(DbDriver, 'getById', mock.MagicMock(return_value='patched'))
    def test_something1(self, mock_obj):
        mock_obj.return_value = '3412424'
        db = DbDriver()
        res = db.getById('dasd')
        print(f'res = {res}')
        # self.assertEquals(True, False)

    # работает
    @patch('src.db.dbDriver.db.connect')
    # @mock.patch.object(DbDriver, 'getById', mock.MagicMock(return_value='patched'))
    def test_something2(self, mock_db):
        mock_db.return_value.cursor.return_value.execute.return_value.fetchone.return_value = ('пососи1',)
        db = DbDriver()
        res = db.getById('фыв')
        print(f'res = {res}')
        # self.assertEqual(True, False)

    def test_smth(self):
        self.assertEqual(True, True)

    @patch('src.db.dbDriver.db')
    # @mock.patch.object(DbDriver, 'getById', mock.MagicMock(return_value='patched'))
    def test_something3(self, mock_db):
        # mock_db.connect.return_value.cursor.return_value.execute.return_value.fetchone.return_value = ('пососи',)
        mock_db.connect().cursor().execute().fetchone.return_value = ('пососи2',)
        db = DbDriver()
        res = db.getById('фыв')
        print(f'res = {res}')
        # self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()

