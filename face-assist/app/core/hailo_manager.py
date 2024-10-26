import os
import subprocess
import logging
from typing import Optional, Tuple, Dict
import json

class HailoManager:
    def __init__(self, hailo_path: str = "/opt/hailo"):
        """Initialize the Hailo manager.
        
        Args:
            hailo_path: Path to Hailo installation
        """
        self.hailo_path = hailo_path
        self.logger = logging.getLogger(__name__)
        self._device_info: Optional[Dict] = None

    def install_runtime(self, package_path: str) -> Tuple[bool, str]:
        """Install Hailo runtime from package.
        
        Args:
            package_path: Path to the Hailo runtime package
            
        Returns:
            Tuple of (success, message)
        """
        try:
            # Run installation script
            result = subprocess.run(
                ['/usr/src/app/scripts/install_hailo.sh'],
                capture_output=True,
                text=True,
                check=True
            )
            self.logger.info("Hailo runtime installed successfully")
            return True, "Installation successful"
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Installation failed: {e.stderr}")
            return False, f"Installation failed: {e.stderr}"
        except Exception as e:
            self.logger.error(f"Unexpected error during installation: {e}")
            return False, f"Unexpected error: {str(e)}"

    def check_device(self) -> Tuple[bool, Dict]:
        """Check Hailo device status.
        
        Returns:
            Tuple of (device_present, device_info)
        """
        try:
            # Check if device exists
            if not os.path.exists("/dev/hailo0"):
                return False, {"error": "Device not found"}

            # Get device info
            result = subprocess.run(
                ['hailort-device-info'],
                capture_output=True,
                text=True
            )

            if result.returncode != 0:
                return False, {"error": "Failed to get device info"}

            # Parse device info
            self._device_info = self._parse_device_info(result.stdout)
            return True, self._device_info

        except Exception as e:
            self.logger.error(f"Error checking device: {e}")
            return False, {"error": str(e)}

    def _parse_device_info(self, info_str: str) -> Dict:
        """Parse device info string into structured data.
        
        Args:
            info_str: Raw device info string
            
        Returns:
            Dictionary containing device information
        """
        try:
            # Basic info parsing - extend based on actual output format
            info = {}
            for line in info_str.split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    info[key.strip()] = value.strip()
            return info
        except Exception as e:
            self.logger.error(f"Error parsing device info: {e}")
            return {"error": "Failed to parse device info"}

    def get_device_temperature(self) -> Optional[float]:
        """Get current device temperature.
        
        Returns:
            Temperature in Celsius or None if unavailable
        """
        try:
            result = subprocess.run(
                ['hailort-device-info', '--temperature'],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                # Parse temperature from output
                temp_str = result.stdout.strip()
                try:
                    return float(temp_str)
                except ValueError:
                    return None
            return None
        except Exception as e:
            self.logger.error(f"Error getting temperature: {e}")
            return None

    def is_runtime_installed(self) -> bool:
        """Check if Hailo runtime is installed.
        
        Returns:
            True if runtime is installed, False otherwise
        """
        try:
            result = subprocess.run(
                ['which', 'hailort-device-info'],
                capture_output=True
            )
            return result.returncode == 0
        except Exception:
            return False
