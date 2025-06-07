# Text-to-Speech (TTS) Application

This application converts text to speech using Next-gen Kaldi. It features a FastAPI backend that provides an API for a Vue.js frontend.

## Project Structure

```
Testupavois/
├── backend/          # Backend specific files
│   ├── __init__.py   # Marks backend as a Python package
│   ├── app.py        # FastAPI backend application (provides API)
│   ├── model.py      # Handles TTS model loading and inference
│   └── requirements.txt # Python dependencies for the backend
├── frontend/         # Vue.js frontend application
│   ├── src/          # Vue source code, including apiService.ts and App.vue
│   ├── public/
│   ├── package.json    # Frontend dependencies and scripts
│   └── vite.config.js  # Vite configuration
├── Dockerfile        # For building the Docker image
├── README.md         # This file (English)
└── README.pt.md      # Portuguese version of this file
```

## Running the Application

There are two ways to run this application: using Docker for the backend or running both backend and frontend locally.

### Option 1: Using Docker (for Backend API)

This method runs the FastAPI backend in a Docker container. The Vue.js frontend will still need to be run locally as described in 'Option 2'.

**Prerequisites:**
*   [Docker](https://docs.docker.com/get-docker/) installed on your system.

**Steps:**

1.  **Build the Docker image:**
    Open a terminal in the project root directory (`Testupavois/`) and run:
    ```bash
    docker build -t tts-app .
    ```

2.  **Run the Docker container:**
    ```bash
    docker run -p 8000:8000 tts-app
    ```

3.  **Access the backend API:**
    The FastAPI backend API will be available at `http://localhost:8000`.
    You can access the interactive API documentation (Swagger UI) at `http://localhost:8000/docs`.
    The Vue.js frontend (run locally) will connect to these API endpoints.

### Option 2: Running Locally (Backend and Frontend)

**Prerequisites:**
*   Python 3.9 or higher
*   Node.js (version 20.x recommended, as per Dockerfile) and npm
*   `wget` (for downloading `espeak-ng-data` if not already present from Docker build)
*   `pip` for Python 3 (Python package manager). If not installed, on Debian/Ubuntu systems, you can install it with: `sudo apt update && sudo apt install python3-pip`

**Backend Setup (Python - FastAPI):**

1.  **Navigate to the project root directory:**
    ```bash
    cd /path/to/Testupavois
    ```

2.  **Create and activate a virtual environment (recommended):**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```
    *Note: The `venv` can be created inside the `backend/` directory or the project root. Adjust paths accordingly.* 

3.  **Install backend dependencies:**
    Ensure `backend/requirements.txt` includes `fastapi`, `uvicorn[standard]`, `python-multipart`, `soundfile`, `sherpa-onnx`, and `huggingface_hub`. (Gradio should be removed).
    ```bash
    python3 -m pip install -r backend/requirements.txt
    ```

4.  **Run the backend application:**
    Navigate to the project root if you aren't already there. The `backend/app.py` script (when run as part of the `backend.app` module) will attempt to download `espeak-ng-data` on its first run if not present.
    From the project root (`Testupavois/`), run:
    ```bash
    python3 -m uvicorn backend.app:app --reload --port 8000
    ```
    The FastAPI backend will be running. You can access:
    *   The API endpoints at `http://localhost:8000/api/...`
    *   The interactive API documentation (Swagger UI) at `http://localhost:8000/docs`.

**Frontend Setup (Vue.js - Vite):**

The Vue.js frontend in the `frontend/` directory provides a custom user interface for the TTS functionality.

1.  **Navigate to the frontend directory:**
    ```bash
    cd /path/to/Testupavois/frontend
    ```

2.  **Install frontend dependencies:**
    ```bash
    npm install
    ```

3.  **Start the frontend development server:**
    ```bash
    npm run dev
    ```
    This will typically start the frontend on a different port (e.g., `http://localhost:5173`). This frontend is configured to make requests to the FastAPI backend running on `http://localhost:8000`.

## How it Works

The backend is built with Python using FastAPI. The `backend/app.py` file sets up the FastAPI application and defines API endpoints (e.g., for listing languages, models, and performing TTS). Core TTS logic and model loading are in `backend/model.py`, utilizing `sherpa-onnx` and pre-trained models downloaded via `huggingface_hub`.

The application downloads `espeak-ng-data` required by some TTS models during the first run of `backend/app.py` or when building the Docker image.

The frontend is a Vue.js application built with Vite. It provides a user interface with controls for language and model selection, text input, and audio playback, interacting with the FastAPI backend via the defined `/api` endpoints.
