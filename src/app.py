from flask import Flask, render_template, request, jsonify, send_from_directory, redirect, url_for
import os
from werkzeug.utils import secure_filename
from deepface import DeepFace
import cv2
import numpy as np
import base64

app=Flask(__name__)

UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploaded')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



@app.route('/')
def home():
    return render_template('index.html')

@app.route('/more-info')
def more_info():
    return render_template('more_info.html')    

@app.route('/option1')
def option1():
    return render_template('option1.html')


@app.route('/option2')
def option2():
    return render_template('option2.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        data = request.get_json()
        image_data = data['image'].split(',')[1]  # base64 image string
        img_bytes = base64.b64decode(image_data)
        np_arr = np.frombuffer(img_bytes, np.uint8)
        frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        result = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
        emotion = result[0]['dominant_emotion']
        return jsonify({'emotion': emotion})
    except Exception as e:
        return jsonify({'emotion': 'No Face Detected', 'error': str(e)})


@app.route('/upload_file', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file:
        filename = secure_filename(file.filename)
        save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(save_path)

        # Predict emotion using DeepFace
        try:
            result = DeepFace.analyze(img_path=save_path, actions=['emotion'], enforce_detection=False)
            emotion = result[0]['dominant_emotion'] if isinstance(result, list) else result['dominant_emotion']
        except Exception as e:
            return jsonify({'error': str(e)}), 500

        return jsonify({
            'filename': filename,
            'url': url_for('uploaded_file', filename=filename),
            'emotion': emotion
        })

    return jsonify({'error': 'File not allowed'}), 400


# Serve uploaded files
@app.route('/uploaded/<path:filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)

