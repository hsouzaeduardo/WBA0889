import unittest
from unittest.mock import patch, MagicMock
from app import app

class GetItemsTests(unittest.TestCase):

    def setUp(self):
        self.app = app
        self.client = self.app.test_client()
        self.app.config['SECRET_KEY'] = '123456789'
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    @patch('app.get_db_connection')
    def test_get_items_success(self, mock_get_db_connection):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_db_connection.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchall.return_value = [
            {'id': 1, 'name': 'Item 1', 'data': 'Data 1', 'quarto': 'Quarto 1', 'avaliacao': 'Avaliacao 1', 'nota': 5},
            {'id': 2, 'name': 'Item 2', 'data': 'Data 2', 'quarto': 'Quarto 2', 'avaliacao': 'Avaliacao 2', 'nota': 4}
        ]

        response = self.client.get('/items')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]['name'], 'Item 1')
        self.assertEqual(data[1]['name'], 'Item 2')

    @patch('app.get_db_connection', side_effect=Exception("Database connection error"))
    def test_get_items_db_connection_error(self, mock_get_db_connection):
        response = self.client.get('/items')
        self.assertEqual(response.status_code, 500)
        self.assertIn('Database connection error', response.data.decode('utf-8'))

if __name__ == '__main__':
    unittest.main()
