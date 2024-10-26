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
        build-base

# Clone and build HailoRT
RUN git clone https://github.com/hailo-ai/hailort.git && \
    cd hailort && \
    mkdir build && \
    cd build && \
    cmake .. && \
    make -j$(nproc) && \
    make install && \
    cd ../.. && \
    rm -rf hailort

# Copy root filesystem
COPY rootfs /

# Set working directory
WORKDIR /usr/share/face-assist

# Copy application files
COPY web /usr/share/face-assist/web
COPY requirements.txt .

# Install Python requirements
RUN pip3 install -r requirements.txt

# Create necessary directories
RUN mkdir -p /share/face-assist/models \
    /share/face-assist/faces \
    /share/face-assist/results

# Expose the port
EXPOSE 8099

# Copy and set up scripts
COPY run.sh /
RUN chmod a+x /run.sh

CMD [ "/run.sh" ]

LABEL \
    io.hass.name="Face Assist" \
    io.hass.description="AI-powered face detection and recognition add-on" \
    io.hass.type="addon" \
    io.hass.version="1.0.0"
