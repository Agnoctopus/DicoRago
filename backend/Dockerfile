# Builder
FROM debian:12.9-slim AS builder
MAINTAINER Agno

# Update and install required packages
RUN apt-get update && \
        apt-get install -y \
            build-essential \
            cmake \
            git \
            python3 \
            python3-pip \
            python3-virtualenv \
            meson \
    && rm -rf /var/lib/apt/lists/*

# Clone the Khaiii repository from GitHub
RUN git clone https://github.com/Agnoctopus/ModernKhaiii.git /opt/khaiii

# Set working directory
WORKDIR /opt/khaiii

# Setup virtualenv
RUN virtualenv env
ENV PATH="/opt/khaiii/env/bin:${PATH}"
RUN pip install --upgrade pip && pip install -r requirements.txt

# Configure conan profile
RUN conan profile detect

# Create build directory and move workdir to
RUN mkdir build
WORKDIR /opt/khaiii/build

# Prepare build
RUN conan install .. --output-folder=. --build=missing
RUN cmake \
    -DCMAKE_TOOLCHAIN_FILE=conan_toolchain.cmake \
    -DCMAKE_BUILD_TYPE=Release \
    -G "Ninja" \
    ..

# Build
RUN cmake --build .
RUN cmake --build . --target large_resource
RUN cmake --build . --target package_python

# Final image
FROM python:3.12-slim
MAINTAINER Agno

# Update and install en_US.UTF-8 locale
RUN apt-get update && \
        apt-get install -y \
            locales \
    && rm -rf /var/lib/apt/lists/*
RUN sed -i 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen && \
    locale-gen && \
    update-locale LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8

# Copy worker build directory
COPY --from=builder /opt/khaiii/ /opt/khaiii/

# Install khaiii
RUN cd /opt/khaiii/build/package_python && pip install .

# Set working directory
WORKDIR /opt/app

# Copy and install requirements
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy project source code
COPY . .

# Expose port 8000 for FastAPI
EXPOSE 8000

# Run the FastAPI application using uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
