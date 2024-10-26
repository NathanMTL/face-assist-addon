ARG BUILD_FROM
FROM ${BUILD_FROM}

# Set shell
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

# Setup base system
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
        jpeg-dev \
        zlib-dev \
        postgresql-dev \
        libxml2-dev \
        libxslt-dev \
        lapack-dev \
        gfortran \
        blas-dev \
        freetype-dev \
        musl-dev

# Copy root filesystem
COPY rootfs /

WORKDIR /opt/face-assist

# Copy app
COPY app /opt/face-assist/app
COPY requirements.txt /opt/face-assist/

# Create required directories
RUN mkdir -p \
    /opt/hailo \
    /share/face-assist/models \
    /share/face-assist/faces \
    /share/face-assist/results \
    /var/log/nginx \
    /var/run/nginx

# Setup Python environment
RUN python3 -m pip install --upgrade pip wheel setuptools
RUN pip3 install --no-cache-dir -r requirements.txt

# Make scripts executable
RUN chmod a+x /etc/services.d/*/run

# Expose port
EXPOSE 8099

# Build arguments
ARG BUILD_VERSION
ARG BUILD_ARCH

# Labels
LABEL \
    io.hass.name="Face Assist" \
    io.hass.description="AI-powered face detection and recognition add-on" \
    io.hass.type="addon" \
    io.hass.version=${BUILD_VERSION} \
    io.hass.arch=${BUILD_ARCH}
