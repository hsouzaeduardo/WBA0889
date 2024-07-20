import io
import pandas as pd
from flask import Flask
import unittest
from unittest.mock import patch, MagicMock
from app import app, upload_file_and_save_json, generate_token

class FlaskAppTests(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        self.token = generate_token({"user_id": 123})

    def get_headers(self):
        return {
            'Authorization': f'Bearer {self.token}'
        }

    @patch('app.sqlite3.connect')
    def test_upload_file_and_save_json_return_error(self, mock_sqlite3):
        response = self.app.post('/upload', headers=self.get_headers())
        self.assertEqual(response.status_code, 400)
        self.assertIn('No file part', response.data.decode('utf-8'))

    @patch('app.sqlite3.connect')
    def test_upload_file_and_save_json_no_file_selected(self, mock_sqlite3):
        data = {'file': (io.BytesIO(b''), '')}
        response = self.app.post('/upload', data=data, content_type='multipart/form-data', headers=self.get_headers())
        self.assertEqual(response.status_code, 400)
        self.assertIn('No selected file', response.data.decode('utf-8'))

    @patch('app.sqlite3.connect')
    def test_upload_file_and_save_json_unsupported_file_type(self, mock_sqlite3):
        data = {'file': (io.BytesIO(b'data'), 'test.txt')}
        response = self.app.post('/upload', data=data, content_type='multipart/form-data', headers=self.get_headers())
        self.assertEqual(response.status_code, 400)
        self.assertIn('Unsupported file type', response.data.decode('utf-8'))

    @patch('app.pd.read_csv')
    @patch('app.sqlite3.connect')
    def test_upload_file_and_save_json_success(self, mock_sqlite3, mock_read_csv):
        df_mock = pd.DataFrame({
            'name': ['item1'],
            'data': ['data1'],
            'quarto': ['quarto1'],
            'avaliacao': ['avaliacao1'],
            'nota': [5]
        })
        mock_read_csv.return_value = df_mock
        
        data = {'file': (io.BytesIO(b'name,data,quarto,avaliacao,nota\nitem1,data1,quarto1,avaliacao1,5'), 'teste.csv')}
        response = self.app.post('/upload', data=data, content_type='multipart/form-data', headers=self.get_headers())
        self.assertEqual(response.status_code, 200)
        self.assertIn('File processed successfully', response.data.decode('utf-8'))

    @patch('app.pd.read_csv', side_effect=Exception("Error processing CSV"))
    @patch('app.sqlite3.connect')
    def test_upload_file_and_save_json_processing_error(self, mock_sqlite3, mock_read_csv):
        data = {'file': (io.BytesIO(b'name,data,quarto,avaliacao,nota\nitem1,data1,quarto1,avaliacao1,5'), 'teste.csv')}
        response = self.app.post('/upload', data=data, content_type='multipart/form-data', headers=self.get_headers())
        self.assertEqual(response.status_code, 500)
        self.assertIn('Error processing CSV', response.data.decode('utf-8'))

    @patch('app.sqlite3.connect')
    def test_upload_file_and_save_json_missing_token(self, mock_sqlite3):
        data = {'file': (io.BytesIO(b'name,data,quarto,avaliacao,nota\nitem1,data1,quarto1,avaliacao1,5'), 'teste.csv')}
        response = self.app.post('/upload', data=data, content_type='multipart/form-data')
        self.assertEqual(response.status_code, 403)
        self.assertIn('Token is missing or invalid', response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
