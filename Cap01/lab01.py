from flask import Flask, request, jsonify
import pandas as pd
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload_file_and_save_json():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    if file and file.filename.endswith('.csv'):
        filename = secure_filename(file.filename)
        #filepath = os.path.join('c:\\temp', filename)  # Para Windows
        #filepath = os.path.join('/tmp', filename)  # Para Unix-like
        file.save(filename)
        
        # Process the CSV file
        df = pd.read_csv(filename)
        json_filename = filename.replace('.csv', '.json')
        df.to_json(json_filename, orient='records')
        # Aqui você pode adicionar o processamento que precisar.
        # Por exemplo, converter em JSON ou inserir em um banco de dados.
        
        # Exemplo: retornar as primeiras 5 linhas do arquivo CSV como JSON
        return jsonify(df.head().to_dict(orient='records'))
    else:
        return jsonify({"error": "Unsupported file type"}), 400

if __name__ == '__main__':
    app.run(debug=True)
