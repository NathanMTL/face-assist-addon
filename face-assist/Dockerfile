ARG BUILD_FROM
FROM $BUILD_FROM

# Set shell
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

# Add required packages
RUN \
    apk update && \
    apk add --no-cache \
        python3 \
        py3-pip \
        nginx \
        gcc \
        g++ \
        make \
        linux-headers \
        python3-dev \
        libffi-dev \
        openssl-dev \
        git \
        cmake \
        build-base \
        tar \
        bash \
        jpeg-dev \
        zlib-dev \
        musl-dev

# Copy root filesystem
COPY rootfs /

# Create required directories
RUN mkdir -p /opt/hailo \
    /share/face-assist/models \
    /share/face-assist/faces \
    /share/face-assist/results \
    /usr/src/app

WORKDIR /usr/src/app

# Copy application files
COPY web /usr/src/app/web
COPY requirements.txt .

# Install Python packages
RUN pip3 install --no-cache-dir -r requirements.txt

# Make scripts executable
RUN chmod a+x /usr/src/app/web/scripts/* || true
RUN chmod a+x /usr/bin/run.sh

# Expose port
EXPOSE 8099

# Labels
LABEL \
    io.hass.name="Face Assist" \
    io.hass.description="AI-powered face detection and recognition add-on" \
    io.hass.type="addon" \
    io.hass.version="1.0.0" \
    io.hass.arch="aarch64" \
    io.hass.docker.params="privileged" 

# Start the application
ENTRYPOINT ["/init"]
CMD []
