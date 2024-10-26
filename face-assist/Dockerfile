ARG BUILD_FROM
FROM ${BUILD_FROM} as builder

# Install build dependencies
RUN \
    apk add --no-cache \
        python3 \
        python3-dev \
        py3-pip \
        gcc \
        g++ \
        make \
        cmake \
        linux-headers \
        libffi-dev \
        openssl-dev \
        git \
        build-base \
        jpeg-dev \
        zlib-dev \
        musl-dev

# Create python virtual environment
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install Python packages in virtual environment
COPY requirements.txt .
RUN pip3 install --no-cache-dir wheel && \
    pip3 install --no-cache-dir -r requirements.txt

# Final stage
FROM ${BUILD_FROM}

# Copy virtual environment from builder
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install runtime dependencies
RUN \
    apk add --no-cache \
        python3 \
        nginx \
        bash \
        tar \
        libstdc++ \
        libgomp \
        jpeg \
        libcrypto3 \
        libssl3

# Create required directories
RUN mkdir -p \
    /opt/hailo \
    /share/face-assist/models \
    /share/face-assist/faces \
    /share/face-assist/results \
    /var/log/nginx \
    /var/run/nginx

# Copy root filesystem
COPY rootfs /

# Set working directory
WORKDIR /usr/src/app

# Copy application files
COPY app /usr/src/app/app
COPY web /usr/src/app/web

# Make scripts executable
RUN chmod a+x /etc/services.d/*/run

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
