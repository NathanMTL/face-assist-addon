#!/usr/bin/with-contenv bashio
# ==============================================================================
# Start Face Assist service
# ==============================================================================

# Wait for Hailo device
bashio::log.info "Waiting for Hailo device..."
while [ ! -e /dev/hailo0 ]; do
    sleep 1
done

cd /usr/src/app

# Start the Flask application
bashio::log.info "Starting Face Assist..."
exec python3 app.py
