from flask import Flask, request, jsonify
import subprocess
import os

app = Flask(__name__)

@app.route('/process', methods=['GET'])
def process_file():
    # Get the file path from the request
    file_url = request.args.get('path')

    if not file_url:
        return jsonify({'error': 'No file path provided'}), 400

    # Ensure the URL scheme is 'file://'
    if not file_url.startswith('file://'):
        return jsonify({'error': 'Invalid file path format'}), 400

    # Extract the actual file path
    file_path = file_url[7:]

    # Check if the file exists
    if not os.path.isfile(file_path):
        return jsonify({'error': 'File does not exist'}), 404

    try:
        # Run the generated_code.py script with the file as an argument
        result = subprocess.run(['python3', 'generated_code.py', file_path], capture_output=True, text=True)

        # Return the output of the script
        return jsonify({'output': result.stdout, 'error': result.stderr})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000, debug=True)