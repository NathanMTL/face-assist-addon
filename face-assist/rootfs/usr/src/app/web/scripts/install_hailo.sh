#!/bin/bash

# Check if Hailo package exists
HAILO_PACKAGE="/opt/hailo/hailort.tar.gz"
if [ ! -f "$HAILO_PACKAGE" ]; then
    echo "Hailo package not found at $HAILO_PACKAGE"
    exit 1
fi

# Extract and install Hailo package
cd /opt/hailo
tar -xzf hailort.tar.gz
cd hailort
./install.sh

# Clean up
cd ..
rm -rf hailort.tar.gz

echo "Hailo installation completed"
