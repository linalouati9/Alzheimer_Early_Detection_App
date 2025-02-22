from flask import Flask, request, jsonify
from flask_cors import CORS
import librosa
import numpy as np

# Import your existing functions and classes here
from script import process_audio_pipeline

app = Flask(__name__)
CORS(app)  # Enable CORS for cross-origin requests (from Flutter)

@app.route('/process-audio', methods=['POST'])
def process_audio():
    try:
        # Access the uploaded file
        audio_file = request.files['file']
        file_path = "temp_audio.wav"  # Temporary path to save the uploaded file
        audio_file.save(file_path)

        # Process the audio file
        predictions = process_audio_pipeline(file_path)
        scalar_value = predictions[0][0]
        print(scalar_value)

        # Determine the result based on the scalar value
        result = 1 if scalar_value > 0.8 else 0

        # Return the result as a response
        return jsonify({'result': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)

