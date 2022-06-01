import unittest
from mock import patch
from src.utils.utils import Utils
# import src.db.dbDriver as db
from src.db.dbDriver import DbDriver
from unittest.mock import Mock


# https://www.reddit.com/r/learnpython/comments/95x8tr/mocking_fetchone_from_sqlite3/
# https://github.com/AndyLPK247/python-testing-101



class MyTestCase(unittest.TestCase):

    # examples

    # @patch('src.db.dbDriver.DbDriver.getById')
    # # @mock.patch.object(DbDriver, 'getById', mock.MagicMock(return_value='patched'))
    # def test_something1(self, mock_obj):
    #     mock_obj.return_value = '3412424'
    #     db = DbDriver(True)
    #     res = db.getById('dasd')
    #     print(f'res = {res}')
    #     # self.assertEquals(True, False)
    #
    # # работает
    # @patch('src.db.dbDriver.db.connect')
    # # @mock.patch.object(DbDriver, 'getById', mock.MagicMock(return_value='patched'))
    # def test_something2(self, mock_db):
    #     mock_db.return_value.cursor.return_value.execute.return_value.fetchone.return_value = ('ololo1',)
    #     db = DbDriver(True)
    #     res = db.getById('фыв')
    #     print(f'res = {res}')
    #     # self.assertEqual(True, False)
    #
    def test_smth(self):
        self.assertEqual(True, True)
    #
    # @patch('src.db.dbDriver.db')
    # # @mock.patch.object(DbDriver, 'getById', mock.MagicMock(return_value='patched'))
    # def test_something3(self, mock_db):
    #     # mock_db.connect.return_value.cursor.return_value.execute.return_value.fetchone.return_value = ('ololo',)
    #     mock_db.connect().cursor().execute().fetchone.return_value = ('ololo2',)
    #     db = DbDriver(True)
    #     res = db.getById('фыв')
    #     print(f'res = {res}')
    #     # self.assertEqual(True, False)
    #
    testsmap = {
        '/add qwe:ewq': True,
        '/add 123d:312 13sd das': True,
        '/add': False,
        '/add dsadsadas': False,
        '/add asdas sdasd:dasd dasd': False,
        '/add asdas sdasd dasd dasd': False,
    }

    @patch('src.utils.utils.DbDriver.add_row_to_mapping')
    @patch('src.utils.utils.Utils.is_admin')
    def test_add_mapping(self, mock_obj, m2):
        mock_obj.return_value = True
        m2.return_value = True
        utils = Utils()
        chat_mock = Mock(id=123)
        m = Mock(chat=chat_mock, text='test')
        for command, result in self.testsmap.items():
            with self.subTest(command=command):
                m.text = command
                print(f' 1 {m.text} - {m.chat.id}')
                r = utils.add_row_to_mapping(m)
                self.assertEqual(r, result)


if __name__ == '__main__':
    unittest.main()

