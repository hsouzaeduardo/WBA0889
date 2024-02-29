from flask import Flask, request, jsonify, make_response
import pandas as pd
from werkzeug.utils import secure_filename
from itsdangerous import URLSafeTimedSerializer
from cachelib.simple import SimpleCache
import time
import functools
import os


# Configuração inicial
SECRET_KEY = "123456789"
serializer = URLSafeTimedSerializer(SECRET_KEY)

# Cria uma instância de cache. Em produção, você pode querer usar algo mais sofisticado como RedisCache.
cache = SimpleCache()
app = Flask(__name__)


def generate_token(data, expiration=300):
    # Gera um token para os dados fornecidos
    token = serializer.dumps(data)
    # Armazena o token no cache com um tempo de expiração (em segundos)
    cache.set(token, data, timeout=expiration)
    return token

def validate_token(token):
    # Tenta recuperar os dados do cache usando o token
    cached_data = cache.get(token)
    if cached_data is not None:
        return cached_data
    return None

def token_required(f):
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]
        if validate_token(token):
            return jsonify({"error": "Token is missing or invalid!"}), 403
        return f(*args, **kwargs)
    return decorated_function

@app.route('/token', methods=['POST'])
def get_token():
    data = {"user_id": 123}
    token = generate_token(data)
    return jsonify({"token": token})

@app.route('/upload', methods=['POST'])
@token_required
def upload_file_and_save_json():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    if file and file.filename.endswith('.csv'):
        filename = secure_filename(file.filename)
        file.save(filename)
        
        # Process the CSV file
        df = pd.read_csv(filename)
        json_filename = filename.replace('.csv', '.json')
        df.to_json(json_filename, orient='records')
        
        return jsonify(df.head().to_dict(orient='records'))
    else:
        return jsonify({"error": "Unsupported file type"}), 400

if __name__ == '__main__':
    app.run(debug=True)
   
