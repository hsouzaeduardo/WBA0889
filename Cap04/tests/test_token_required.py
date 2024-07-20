import unittest
from unittest.mock import patch, MagicMock
from flask import jsonify
from app import app, token_required, generate_token

# Criação de uma rota protegida para testar o decorador
@app.route('/protected')
@token_required
def protected_route():
    return jsonify({'message': 'This is a protected route'}), 200

class TokenRequiredTests(unittest.TestCase):

    def setUp(self):
        self.app = app
        self.client = self.app.test_client()
        self.app.config['SECRET_KEY'] = '123456789'
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    @patch('app.validate_token')
    def test_token_required_valid_token(self, mock_validate_token):
        mock_validate_token.return_value = {"user_id": 123}
        token = generate_token({"user_id": 123})

        headers = {
            'Authorization': f'Bearer {token}'
        }
        response = self.client.get('/protected', headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertIn('This is a protected route', response.data.decode('utf-8'))

    @patch('app.validate_token')
    def test_token_required_invalid_token(self, mock_validate_token):
        mock_validate_token.return_value = None
        token = "invalid_token"

        headers = {
            'Authorization': f'Bearer {token}'
        }
        response = self.client.get('/protected', headers=headers)
        self.assertEqual(response.status_code, 403)
        self.assertIn('Token is missing or invalid', response.data.decode('utf-8'))

    def test_token_required_missing_token(self):
        response = self.client.get('/protected')
        self.assertEqual(response.status_code, 403)
        self.assertIn('Token is missing or invalid', response.data.decode('utf-8'))

if __name__ == '__main__':
    unittest.main()
