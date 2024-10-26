import os
import json

# Load Home Assistant Add-on configuration
def load_config():
    try:
        with open('/data/options.json') as config_file:
            return json.load(config_file)
    except Exception as e:
        print(f"Error loading config: {e}")
        return get_default_config()

def get_default_config():
    return {
        "models_path": "/share/face-assist/models",
        "faces_path": "/share/face-assist/faces",
        "results_path": "/share/face-assist/results",
        "max_model_size": 500,
        "supported_model_formats": [".onnx", ".tflite"],
        "log_level": "info"
    }

# Load configuration
CONFIG = load_config()

# Paths
MODELS_PATH = CONFIG.get('models_path', '/share/face-assist/models')
FACES_PATH = CONFIG.get('faces_path', '/share/face-assist/faces')
RESULTS_PATH = CONFIG.get('results_path', '/share/face-assist/results')
HAILO_PATH = "/opt/hailo"

# Model settings
MAX_MODEL_SIZE = CONFIG.get('max_model_size', 500) * 1024 * 1024  # Convert to bytes
SUPPORTED_FORMATS = CONFIG.get('supported_model_formats', [".onnx", ".tflite"])

# API settings
API_HOST = "0.0.0.0"
API_PORT = 8099

# Logging
LOG_LEVEL = CONFIG.get('log_level', 'info').upper()

# Face recognition settings
FACE_MATCH_THRESHOLD = 0.6
CONFIDENCE_THRESHOLD = 80.0
