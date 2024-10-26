#!/bin/bash

# Check if Hailo package exists
HAILO_PACKAGE="/opt/hailo/hailort.tar.gz"
if [ ! -f "$HAILO_PACKAGE" ]; then
    echo "Hailo package not found at $HAILO_PACKAGE"
    exit 1
fi

# Create temporary directory
mkdir -p /opt/hailo/temp
cd /opt/hailo/temp

# Extract and install Hailo package
tar -xzf ../hailort.tar.gz

# Run installation
if [ -f "./install.sh" ]; then
    chmod +x ./install.sh
    ./install.sh
elif [ -f "./hailort/install.sh" ]; then
    chmod +x ./hailort/install.sh
    ./hailort/install.sh
else
    echo "Could not find install.sh script"
    exit 1
fi

# Clean up
cd ..
rm -rf temp hailort.tar.gz

echo "Hailo installation completed"
