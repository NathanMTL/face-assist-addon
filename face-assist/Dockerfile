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
        wget \
        tar \
        curl

# Install Hailo Runtime (using latest version 4.19.0)
RUN wget https://hailo-hailort.s3.eu-west-2.amazonaws.com/HailoRT/v4.19.0/hailort-aarch64-4.19.0/hailort_4.19.0_aarch64.tar.gz && \
    tar -xzf hailort_4.19.0_aarch64.tar.gz && \
    cd hailort && \
    ./install.sh && \
    cd .. && \
    rm -rf hailort*

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
