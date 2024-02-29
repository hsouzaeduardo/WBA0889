import io
from flask import Flask
import unittest
from unittest.mock import patch
from app import app, upload_file_and_save_json

class FlaskAppTests(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    @patch('lab04.sqlite3.connect')
    def test_upload_file_and_save_json_return_error(self, mock_sqlite3):
        response = self.app.post('/upload')
        self.assertEqual(response.status_code, 403)
        
    def test_upload_file_return_ok(self, mock_upload):
        mock_upload.return_value = 'Simulação de upload'
        response = self.app.post('/upload', data={
            'file': (io.BytesIO(b'Meu,csv,simulado'), 'teste.csv'),
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('Simulação de upload', response.data.decode('utf-8'))