import unittest
from app import app, generate_token
from itsdangerous import URLSafeTimedSerializer

class GenerateTokenTests(unittest.TestCase):

    def setUp(self):
        self.app = app
        self.app.config['SECRET_KEY'] = '123456789'
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.serializer = URLSafeTimedSerializer(self.app.config['SECRET_KEY'])

    def tearDown(self):
        self.app_context.pop()

    def test_generate_token_success(self):
        data = {"user_id": 123}
        token = generate_token(data)
        self.assertIsNotNone(token)

    def test_generate_token_expiration(self):
        data = {"user_id": 123}
        token = generate_token(data, expiration=10)
        self.assertIsNotNone(token)

    def test_generate_token_data_integrity(self):
        data = {"user_id": 123}
        token = generate_token(data)
        decoded_data = self.serializer.loads(token)
        self.assertEqual(decoded_data, data)

if __name__ == '__main__':
    unittest.main()
