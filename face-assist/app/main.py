from flask import Flask
import logging
import os
from api.routes import api, web
from config.default_config import (
    API_HOST, API_PORT, LOG_LEVEL,
    MODELS_PATH, FACES_PATH, RESULTS_PATH
)

def create_app():
    """Create and configure the Flask application"""
    # Initialize Flask app
    app = Flask(__name__)
    
    # Configure logging
    logging.basicConfig(
        level=getattr(logging, LOG_LEVEL),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Ensure required directories exist
    for path in [MODELS_PATH, FACES_PATH, RESULTS_PATH]:
        os.makedirs(path, exist_ok=True)
    
    # Register blueprints
    app.register_blueprint(web)
    app.register_blueprint(api, url_prefix='/api')
    
    return app

def main():
    """Main entry point for the application"""
    app = create_app()
    app.run(host=API_HOST, port=API_PORT)

if __name__ == '__main__':
    main()
