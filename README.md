# Face Assist Add-on for Home Assistant

AI-powered face detection and recognition add-on with user-friendly web interface.

## Features

- Drag-and-drop model management
- Easy face database creation and management
- Real-time face verification
- Optimized for Hailo8L NPU
- Clean, modern web interface
- Comprehensive documentation

## Requirements

### Hardware
- Raspberry Pi 5 (8GB)
- M.2 HAT with Hailo8L chip
- Home Assistant OS

### Software
- Home Assistant OS
- Hailo Runtime

## Installation

1. In Home Assistant, navigate to **Settings** → **Add-ons** → **Add-on Store**
2. Click the menu (⋮) in the top right and select **Repositories**
3. Add this repository URL:
   ```
   https://github.com/nathanmtl/face-assist-addon
   ```
4. Click **Add**
5. Find "Face Assist" in the add-on store and click **Install**

## Configuration

Minimum configuration in your Home Assistant installation:

```yaml
models_path: "/share/face-assist/models"
faces_path: "/share/face-assist/faces"
results_path: "/share/face-assist/results"
```

## Usage

1. Install the add-on
2. Start it and access the web interface
3. Upload your AI models
4. Add faces to the database
5. Use the verification system to match faces

## Support

For issues and feature requests, please open an issue on GitHub.

## License

MIT License
