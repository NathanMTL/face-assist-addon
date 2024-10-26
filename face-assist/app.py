from flask import Flask, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
import os
import json
import cv2
import numpy as np
import face_recognition
from PIL import Image
import shutil
import subprocess

app = Flask(__name__, static_folder='web')

# Configuration
CONFIG_FILE = '/data/options.json'
with open(CONFIG_FILE) as config_file:
    config = json.load(config_file)

MODELS_PATH = config['models_path']
FACES_PATH = config['faces_path']
RESULTS_PATH = config['results_path']
MAX_MODEL_SIZE = config['max_model_size'] * 1024 * 1024  # Convert to bytes
SUPPORTED_FORMATS = config['supported_model_formats']

# Ensure directories exist
os.makedirs(MODELS_PATH, exist_ok=True)
os.makedirs(FACES_PATH, exist_ok=True)
os.makedirs(RESULTS_PATH, exist_ok=True)
os.makedirs('/opt/hailo', exist_ok=True)

# Known faces database
known_faces = {}

def load_known_faces():
    """Load all known faces from the faces directory"""
    for person_dir in os.listdir(FACES_PATH):
        person_path = os.path.join(FACES_PATH, person_dir)
        if os.path.isdir(person_path):
            encodings = []
            for img_file in os.listdir(person_path):
                if img_file.lower().endswith(('.png', '.jpg', '.jpeg')):
                    img_path = os.path.join(person_path, img_file)
                    image = face_recognition.load_image_file(img_path)
                    face_encodings = face_recognition.face_encodings(image)
                    if face_encodings:
                        encodings.extend(face_encodings)
            if encodings:
                known_faces[person_dir] = encodings

@app.route('/')
def index():
    return send_from_directory('web', 'index.html')

@app.route('/api/models', methods=['GET'])
def list_models():
    """List all uploaded models"""
    models = []
    for model in os.listdir(MODELS_PATH):
        if any(model.endswith(fmt) for fmt in SUPPORTED_FORMATS):
            models.append({
                'name': model,
                'size': os.path.getsize(os.path.join(MODELS_PATH, model))
            })
    return jsonify(models)

@app.route('/api/upload/model', methods=['POST'])
def upload_model():
    """Handle model upload"""
    if 'model' not in request.files:
        return jsonify({'error': 'No model file provided'}), 400
    
    model_file = request.files['model']
    if not any(model_file.filename.endswith(fmt) for fmt in SUPPORTED_FORMATS):
        return jsonify({'error': 'Unsupported model format'}), 400
    
    if model_file.content_length > MAX_MODEL_SIZE:
        return jsonify({'error': 'Model file too large'}), 400
    
    filename = secure_filename(model_file.filename)
    model_file.save(os.path.join(MODELS_PATH, filename))
    return jsonify({'message': 'Model uploaded successfully'})

@app.route('/api/faces', methods=['GET'])
def list_faces():
    """List all registered faces"""
    faces = []
    for person in os.listdir(FACES_PATH):
        if os.path.isdir(os.path.join(FACES_PATH, person)):
            faces.append({
                'name': person,
                'image_count': len(os.listdir(os.path.join(FACES_PATH, person)))
            })
    return jsonify(faces)

@app.route('/api/faces/<person>', methods=['POST'])
def add_face(person):
    """Add a new face image for a person"""
    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400
    
    image_file = request.files['image']
    if not image_file.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        return jsonify({'error': 'Unsupported image format'}), 400
    
    person_dir = os.path.join(FACES_PATH, secure_filename(person))
    os.makedirs(person_dir, exist_ok=True)
    
    filename = secure_filename(image_file.filename)
    image_path = os.path.join(person_dir, filename)
    image_file.save(image_path)
    
    # Process the face
    image = face_recognition.load_image_file(image_path)
    face_encodings = face_recognition.face_encodings(image)
    
    if not face_encodings:
        os.remove(image_path)
        return jsonify({'error': 'No face detected in image'}), 400
    
    if person not in known_faces:
        known_faces[person] = []
    known_faces[person].extend(face_encodings)
    
    return jsonify({'message': 'Face added successfully'})

@app.route('/api/verify', methods=['POST'])
def verify_face():
    """Verify if a face matches a known person"""
    if 'image' not in request.files or 'person' not in request.form:
        return jsonify({'error': 'Missing image or person name'}), 400
    
    image_file = request.files['image']
    person = request.form['person']
    
    if person not in known_faces:
        return jsonify({'error': 'Person not found'}), 404
    
    # Process the verification image
    image = face_recognition.load_image_file(image_file)
    face_encodings = face_recognition.face_encodings(image)
    
    if not face_encodings:
        return jsonify({'error': 'No face detected in image'}), 400
    
    # Compare with known faces
    matches = face_recognition.compare_faces(known_faces[person], face_encodings[0])
    match_percentage = (sum(matches) / len(matches)) * 100 if matches else 0
    
    return jsonify({
        'match': match_percentage >= 80,
        'confidence': match_percentage
    })

@app.route('/api/hailo/upload', methods=['POST'])
def upload_hailo():
    """Handle Hailo runtime package upload"""
    if 'package' not in request.files:
        return jsonify({'error': 'No package file provided'}), 400
    
    package_file = request.files['package']
    if not package_file.filename.endswith('.tar.gz'):
        return jsonify({'error': 'Invalid package format'}), 400
    
    # Save the package
    package_path = '/opt/hailo/hailort.tar.gz'
    package_file.save(package_path)
    
    try:
        # Run installation script
        result = subprocess.run(['/usr/src/app/web/scripts/install_hailo.sh'], 
                              capture_output=True, text=True, check=True)
        return jsonify({
            'message': 'Hailo runtime installed successfully',
            'details': result.stdout
        })
    except subprocess.CalledProcessError as e:
        return jsonify({
            'error': 'Installation failed',
            'details': e.stderr
        }), 500

@app.route('/api/hailo/status', methods=['GET'])
def hailo_status():
    """Check Hailo runtime status"""
    try:
        result = subprocess.run(['hailort-device-info'], 
                              capture_output=True, text=True)
        return jsonify({
            'installed': True,
            'details': result.stdout
        })
    except:
        return jsonify({
            'installed': False
        })

# Initialize face database on startup
load_known_faces()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8099)
