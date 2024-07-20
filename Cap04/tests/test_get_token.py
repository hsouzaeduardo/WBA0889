import unittest
from unittest.mock import patch
from app import app, generate_token

class GetTokenTests(unittest.TestCase):

    def setUp(self):
        self.app = app
        self.client = self.app.test_client()
        self.app.config['SECRET_KEY'] = '123456789'
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    @patch('app.generate_token')
    def test_get_token_success(self, mock_generate_token):
        mock_generate_token.return_value = "fake_token"

        response = self.client.post('/token')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('token', data)
        self.assertEqual(data['token'], "fake_token")

    @patch('app.generate_token', side_effect=Exception("Token generation error"))
    def test_get_token_error(self, mock_generate_token):
        response = self.client.post('/token')
        self.assertEqual(response.status_code, 500)
        self.assertIn('Token generation error', response.data.decode('utf-8'))

if __name__ == '__main__':
    unittest.main()
