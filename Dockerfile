# Multi-stage build for production
# Stage 1: Build frontend
FROM node:20-alpine AS frontend-builder

WORKDIR /app/frontend

# Copy package files
COPY frontend/package*.json ./

# Install dependencies (including devDependencies for build)
RUN npm ci

# Copy source code
COPY frontend/ ./

# Build the application
RUN npm run build

# Stage 2: Setup Python backend with frontend
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    wget \
    build-essential \
    git \
    libreoffice \
    && rm -rf /var/lib/apt/lists/*

# Copy the backend requirements file and install dependencies
COPY backend/requirements.txt /app/backend/
RUN pip install --no-cache-dir -r backend/requirements.txt

# Install additional required packages
RUN pip install --no-cache-dir huggingface_hub python-docx PyPDF2 python-pptx

# Download espeak-ng-data
RUN wget -qO- https://github.com/k2-fsa/sherpa-onnx/releases/download/tts-models/espeak-ng-data.tar.bz2 | tar -xj -C /tmp
ENV ESPNET_TTS_ESPEAK_NG_DICT_DIR /tmp/espeak-ng-data

# Copy backend application code
COPY backend /app/backend

# Copy built frontend from the previous stage
COPY --from=frontend-builder /app/frontend/dist /app/static

# Copy startup script
COPY start.sh /app/start.sh
RUN chmod +x /app/start.sh

# Expose the port
EXPOSE 8000

# Command to run the application
CMD ["/app/start.sh"]
