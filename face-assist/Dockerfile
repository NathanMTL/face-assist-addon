ARG BUILD_FROM
FROM ${BUILD_FROM}

# Install required packages
RUN \
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
        bash

# Create required directories
RUN mkdir -p /opt/hailo \
    /share/face-assist/models \
    /share/face-assist/faces \
    /share/face-assist/results

# Set working directory
WORKDIR /usr/src/app

# Copy application files
COPY web /usr/src/app/web
COPY requirements.txt .
COPY rootfs /

# Install Python packages
RUN pip3 install --no-cache-dir -r requirements.txt

# Make scripts executable
RUN chmod a+x /usr/src/app/web/scripts/* || true
RUN chmod a+x /run.sh

# Expose port
EXPOSE 8099

# Start the application
CMD [ "/run.sh" ]

LABEL \
    io.hass.name="Face Assist" \
    io.hass.description="AI-powered face detection and recognition add-on" \
    io.hass.type="addon" \
    io.hass.version="1.0.0"
