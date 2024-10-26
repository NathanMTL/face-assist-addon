# Face Assist Add-on Documentation

## Overview
Face Assist is an AI-powered face detection and recognition add-on for Home Assistant. It utilizes the Hailo8L NPU for efficient AI processing on your Raspberry Pi 5.

## Prerequisites

### Hardware Requirements
- Raspberry Pi 5 (8GB RAM model)
- M.2 HAT with Hailo8L chip
- Sufficient storage space (minimum 2GB recommended)

### Software Requirements
- Home Assistant OS
- Access to the Hailo Runtime package

## Installation

1. Add the repository to your Home Assistant instance:
   ```
   https://github.com/nathanmtl/face-assist-addon
   ```
2. Install the Face Assist add-on
3. Start the add-on
4. Open the web interface

## Configuration

### Add-on Configuration Options

| Option | Description | Default |
|--------|-------------|---------|
| models_path | Path to store AI models | `/share/face-assist/models` |
| faces_path | Path to store face database | `/share/face-assist/faces` |
| results_path | Path to store results | `/share/face-assist/results` |
| max_model_size | Maximum model size in MB | 500 |
| log_level | Logging level | info |

Example configuration:
```yaml
models_path: "/share/face-assist/models"
faces_path: "/share/face-assist/faces"
results_path: "/share/face-assist/results"
max_model_size: 500
log_level: "info"
```

## Usage

### Initial Setup
1. After starting the add-on, navigate to the web interface
2. Upload the Hailo Runtime package if not already installed
3. Add face recognition models to the Models section
4. Create face database entries in the Faces section

### Adding Faces
1. Enter the person's name
2. Upload clear photos of their face
3. Use multiple angles for better recognition
4. Minimum recommended: 3 photos per person

### Face Verification
1. Select a person from the database
2. Upload a photo to verify
3. View match results and confidence score

## Model Requirements

### Supported Formats
- ONNX (.onnx)
- TensorFlow Lite (.tflite)

### Model Specifications
- Maximum file size: 500MB
- Optimized for Hailo8L NPU
- Input size: 640x480 to 1920x1080

## Image Requirements

### Supported Formats
- JPEG (.jpg, .jpeg)
- PNG (.png)

### Recommendations
- Resolution: 640x480 to 1920x1080
- Clear, well-lit faces
- Multiple angles per person
- Unobstructed view of face
- Neutral expressions
- Maximum file size: 10MB

## Network Access
The add-on requires access to:
- Port 8099 for web interface
- Home Assistant API
- Supervisor API

## Hardware Access
The add-on requires access to:
- Hailo device (/dev/hailo0)
- System resources for AI processing

## Troubleshooting

### Common Issues

1. Hailo Device Not Found
   - Check if the Hailo8L chip is properly connected
   - Verify the M.2 HAT installation
   - Check system logs for hardware detection

2. Model Upload Fails
   - Verify file size is under 500MB
   - Ensure model format is supported
   - Check available storage space

3. Face Detection Issues
   - Ensure image meets quality requirements
   - Check lighting conditions
   - Verify face is clearly visible

4. Performance Issues
   - Check system resource usage
   - Verify Hailo Runtime is properly installed
   - Monitor temperature of Raspberry Pi

### Logs
To view addon logs:
1. Go to Supervisor → Face Assist → Logs
2. Set log_level for more detailed information

## Support

### Getting Help
- GitHub Issues: Report bugs and request features
- Documentation: Latest updates and guides
- Home Assistant Community: Discussion and tips

### Reporting Issues
When reporting issues, please include:
- Add-on version
- Home Assistant version
- Hardware configuration
- Relevant logs
- Steps to reproduce

## Security
- All data is stored locally
- No cloud services required
- Regular security updates
- AppArmor enabled

## Backup
The add-on uses the following paths that should be included in backups:
- /share/face-assist/models
- /share/face-assist/faces
- /share/face-assist/results

## License
MIT License - See LICENSE file for details
