#!/usr/bin/with-contenv bashio
set -e

# Configure Nginx
bashio::log.info "Configuring Nginx..."
mkdir -p /var/log/nginx
touch /var/log/nginx/error.log
chown -R nginx:nginx /var/log/nginx

# Start Nginx in background
nginx &

# Start Face Assist application
bashio::log.info "Starting Face Assist..."
cd /usr/share/face-assist
python3 app.py
