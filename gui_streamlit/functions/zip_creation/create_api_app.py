
def create_api_app(temp_path):
    # Python script to create an API app
    api_app_content ="""
from flask import Flask, request, jsonify
import subprocess
import os
import json

app = Flask(__name__)

@app.route('/process', methods=['POST'])
def process_file():
    # Check if a file is provided in the request
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    uploaded_file = request.files['file']
    
    if uploaded_file.filename == '':
        return jsonify({'error': 'Empty file name'}), 400
    
    # Save file temporarily
    temp_path = os.path.join('/tmp', uploaded_file.filename)
    uploaded_file.save(temp_path)
    
    try:
        # Run the Generated_Code.py script with the file as an argument
        result = subprocess.run(['python3', 'Generated_Code.py', temp_path], capture_output=True, text=True)
        
        # Remove the temporary file after processing
        os.remove(temp_path)
        
        # Try to parse the output as JSON
        try:
            output_json = json.loads(result.stdout)  # Parse the captured output
            return jsonify({'file_name': uploaded_file.filename, 'output': output_json})
        except json.JSONDecodeError:
            return jsonify({'file_name': uploaded_file.filename, 'error': result.stderr}), 500
         
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000, debug=True)
"""

    with open(f'{temp_path}/app.py', "w") as app_file:
        app_file.write(api_app_content)

    return f'{temp_path}/app.py'