import unittest
import time
from app import app, generate_token, validate_token
from itsdangerous import URLSafeTimedSerializer

class ValidateTokenTests(unittest.TestCase):

    def setUp(self):
        self.app = app
        self.app.config['SECRET_KEY'] = '123456789'
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.serializer = URLSafeTimedSerializer(self.app.config['SECRET_KEY'])

    def tearDown(self):
        self.app_context.pop()

    def test_validate_token_success(self):
        data = {"user_id": 123}
        token = generate_token(data)
        validated_data = validate_token(token)
        self.assertEqual(validated_data, data)

    def test_validate_token_invalid(self):
        invalid_token = "invalid.token"
        validated_data = validate_token(invalid_token)
        self.assertIsNone(validated_data)

    def test_validate_token_expired(self):
        data = {"user_id": 123}
        token = generate_token(data, expiration=1)
        time.sleep(2)
        validated_data = validate_token(token)
        self.assertIsNone(validated_data)

if __name__ == '__main__':
    unittest.main()