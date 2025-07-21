#!/bin/bash

# Start script for TTS Application

echo "Starting TTS Application..."
echo "Current directory: $(pwd)"
echo "Available files:"
ls -la

# Check if static directory exists
if [ -d "/app/static" ]; then
    echo "Static files found:"
    ls -la /app/static/
else
    echo "Warning: Static directory not found. Frontend may not be available."
fi

# Check if backend exists
if [ -d "/app/backend" ]; then
    echo "Backend directory found"
else
    echo "Error: Backend directory not found!"
    exit 1
fi

# Set environment variables
export PYTHONPATH=/app:$PYTHONPATH

# Wait a moment for any system initialization
sleep 2

echo "Starting FastAPI server..."

# Start the application
exec python3 -m uvicorn backend.app:app --host 0.0.0.0 --port 8000 --workers 1
