from flask import Blueprint, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
import os
from ..core.face_processor import FaceProcessor
from ..core.hailo_manager import HailoManager
from ..config.default_config import (
    MODELS_PATH, FACES_PATH, RESULTS_PATH,
    MAX_MODEL_SIZE, SUPPORTED_FORMATS
)

# Create blueprints
api = Blueprint('api', __name__)
web = Blueprint('web', __name__, static_folder='web')

# Initialize processors
face_processor = FaceProcessor(FACES_PATH)
hailo_manager = HailoManager()

@web.route('/')
def index():
    return send_from_directory('web', 'index.html')

@api.route('/models', methods=['GET'])
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

@api.route('/upload/model', methods=['POST'])
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

@api.route('/faces', methods=['GET'])
def list_faces():
    """List all registered faces"""
    return jsonify(face_processor.list_people())

@api.route('/faces/<person>', methods=['POST'])
def add_face(person):
    """Add a new face image for a person"""
    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400
    
    image_file = request.files['image']
    if not image_file.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        return jsonify({'error': 'Unsupported image format'}), 400
    
    # Save the image temporarily
    temp_path = os.path.join(FACES_PATH, secure_filename(person), secure_filename(image_file.filename))
    os.makedirs(os.path.dirname(temp_path), exist_ok=True)
    image_file.save(temp_path)
    
    # Process the face
    success, message = face_processor.add_face(person, temp_path)
    
    if not success:
        os.remove(temp_path)
        return jsonify({'error': message}), 400
    
    return jsonify({'message': message})

@api.route('/verify', methods=['POST'])
def verify_face():
    """Verify if a face matches a known person"""
    if 'image' not in request.files or 'person' not in request.form:
        return jsonify({'error': 'Missing image or person name'}), 400
    
    image_file = request.files['image']
    person = request.form['person']
    
    # Save the image temporarily
    temp_path = os.path.join(RESULTS_PATH, 'temp_verify.jpg')
    image_file.save(temp_path)
    
    # Verify the face
    match, confidence = face_processor.verify_face(person, temp_path)
    
    # Clean up
    os.remove(temp_path)
    
    return jsonify({
        'match': match,
        'confidence': confidence
    })

@api.route('/hailo/status', methods=['GET'])
def hailo_status():
    """Check Hailo device status"""
    is_installed = hailo_manager.is_runtime_installed()
    if not is_installed:
        return jsonify({
            'installed': False,
            'message': 'Hailo runtime not installed'
        })
    
    device_present, device_info = hailo_manager.check_device()
    return jsonify({
        'installed': True,
        'device_present': device_present,
        'device_info': device_info,
        'temperature': hailo_manager.get_device_temperature()
    })

@api.route('/hailo/upload', methods=['POST'])
def upload_hailo():
    """Handle Hailo runtime package upload"""
    if 'package' not in request.files:
        return jsonify({'error': 'No package file provided'}), 400
    
    package_file = request.files['package']
    if not package_file.filename.endswith('.tar.gz'):
        return jsonify({'error': 'Invalid package format'}), 400
    
    # Save the package
    package_path = os.path.join(RESULTS_PATH, 'hailort.tar.gz')
    package_file.save(package_path)
    
    # Install the runtime
    success, message = hailo_manager.install_runtime(package_path)
    
    # Clean up
    os.remove(package_path)
    
    if not success:
        return jsonify({'error': message}), 500
        
    return jsonify({'message': message})
