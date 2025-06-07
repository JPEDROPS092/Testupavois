# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
# - wget for downloading espeak-ng-data
# - build-essential for some python packages that might need compilation
# - git for any potential git-based python package installations
# - libreoffice for document processing
RUN apt-get update && apt-get install -y \
    wget \
    build-essential \
    git \
    libreoffice \
    && rm -rf /var/lib/apt/lists/*

# Install Node.js and npm for frontend
RUN apt-get update && apt-get install -y ca-certificates curl gnupg && \
    mkdir -p /etc/apt/keyrings && \
    curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key | gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg && \
    NODE_MAJOR=20 && \
    echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_$NODE_MAJOR.x nodistro main" | tee /etc/apt/sources.list.d/nodesource.list && \
    apt-get update && apt-get install nodejs -y && \
    rm -rf /var/lib/apt/lists/*

# Copy the backend requirements file and install dependencies
COPY backend/requirements.txt /app/backend/
RUN pip install --no-cache-dir -r backend/requirements.txt

# Install huggingface_hub as it's missing from requirements.txt but imported in model.py
# Install document processing libraries
RUN pip install --no-cache-dir huggingface_hub python-docx PyPDF2 python-pptx

# Copy backend application code (which now includes app.py, model.py, __init__.py)
# The requirements.txt is already copied and installed.
COPY backend /app/backend

# Download espeak-ng-data as done in app.py
RUN wget -qO- https://github.com/k2-fsa/sherpa-onnx/releases/download/tts-models/espeak-ng-data.tar.bz2 | tar -xj -C /tmp
ENV ESPNET_TTS_ESPEAK_NG_DICT_DIR /tmp/espeak-ng-data

# Copy frontend application code
COPY frontend /app/frontend

# Install frontend dependencies and build
WORKDIR /app/frontend
RUN npm install
RUN npm run build

# Go back to the app root for running the backend
WORKDIR /app

# Expose the port the FastAPI server runs on
EXPOSE 8000

# Command to run the application
# The Gradio app.py uses demo.launch() which by default might not bind to 0.0.0.0
# We need to ensure it binds to 0.0.0.0 to be accessible from outside the container.
# Also, the frontend build needs to be served or app.py needs to know where it is.
# For Gradio, app.py typically serves its own frontend. The `npm run build` for the Vue app
# might be for a scenario where the Vue app communicates with the Gradio backend as an API.
# For now, assuming Gradio serves everything and the Vue app might be a separate way to interact or was for a different setup.
# If app.py needs to serve the Vue built files, this CMD needs adjustment.
CMD ["python3", "-m", "uvicorn", "backend.app:app", "--host", "0.0.0.0", "--port", "8000"]
