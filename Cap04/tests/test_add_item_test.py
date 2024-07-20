import unittest
from unittest.mock import patch, MagicMock
from app import app, add_item, init_db

class AddItemTests(unittest.TestCase):

    def setUp(self):
        self.app = app
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    @patch('app.get_db_connection')
    def test_add_item_success(self, mock_get_db_connection):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_db_connection.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        initdb = init_db();
        response = add_item('NomeTeste', 'DataTeste', 'QuartoTeste', 'AvaliaçãoTeste', 5)
        self.assertEqual(response[0].json, {'status': 'success', 'name': 'NomeTeste'})
        self.assertEqual(response[1], 201)
        mock_cursor.execute.assert_called_once_with('INSERT INTO items (name, data, quarto, avaliacao, nota) VALUES (?, ?, ?, ?, ?)', 
                                                    ('NomeTeste', 'DataTeste', 'QuartoTeste', 'AvaliaçãoTeste', 5))
        mock_conn.commit.assert_called_once()
        mock_conn.close.assert_called_once()

    @patch('app.get_db_connection', side_effect=Exception("Database connection error"))
    def test_add_item_db_connection_error(self, mock_get_db_connection):
        response = add_item('NomeTeste', 'DataTeste', 'QuartoTeste', 'AvaliaçãoTeste', 5)
        self.assertEqual(response[0].json, {'error': 'Database connection error'})
        self.assertEqual(response[1], 500)

    @patch('app.get_db_connection')
    def test_add_item_sql_error(self, mock_get_db_connection):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_db_connection.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.execute.side_effect = Exception("SQL error")

        response = add_item('NomeTeste', 'DataTeste', 'QuartoTeste', 'AvaliaçãoTeste', 5)
        self.assertEqual(response[0].json, {'error': 'SQL error'})
        self.assertEqual(response[1], 500)

if __name__ == '__main__':
    unittest.main()
