# Face Assist Add-on for Home Assistant

AI-powered face detection and recognition add-on with user-friendly web interface.

## Installation

1. In Home Assistant, navigate to **Settings** → **Add-ons** → **Add-on Store**
2. Click the menu (⋮) in the top right and select **Repositories**
3. Add this repository URL:
   ```
   https://github.com/yourusername/face-assist-addon
   ```
4. Click **Add**
5. Find "Face Assist" in the add-on store and click **Install**

## Requirements

- Raspberry Pi 5 (8GB)
- M.2 HAT with Hailo8L chip
- Home Assistant OS

## Configuration

1. Set up storage paths in the add-on configuration:
   ```yaml
   models_path: "/share/face-assist/models"
   faces_path: "/share/face-assist/faces"
   results_path: "/share/face-assist/results"
   ```

2. Start the add-on and open the web interface

## Support

For issues and feature requests, please open an issue on GitHub.
