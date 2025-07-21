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

There are three ways to run this application: using Docker Compose (recommended), using Docker manually, or running both backend and frontend locally.

### Option 1: Using Docker Compose (Recommended)

This is the easiest way to run the complete application with both frontend and backend in a single container.

**Prerequisites:**

- [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/) installed on your system.

**Steps:**

1.  **Clone and navigate to the project directory:**

    ```bash
    cd /path/to/Testupavois
    ```

2.  **Build and run the application:**

    ```bash
    docker-compose up --build
    ```

    Or run in background:

    ```bash
    docker-compose up -d --build
    ```

3.  **Access the application:**

    - Frontend UI: `http://localhost:8000`
    - API documentation: `http://localhost:8000/docs`
    - API endpoints: `http://localhost:8000/api/...`

4.  **Stop the application:**
    ```bash
    docker-compose down
    ```

### Option 2: Using Docker Manually

**Prerequisites:**

- [Docker](https://docs.docker.com/get-docker/) installed on your system.

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

3.  **Access the application:**
    - Frontend UI: `http://localhost:8000`
    - API documentation: `http://localhost:8000/docs`
    - API endpoints: `http://localhost:8000/api/...`

### Option 3: Running Locally (Backend and Frontend Separately)

This option is recommended for development purposes.

**Prerequisites:**

- Python 3.9 or higher
- Node.js (version 20.x recommended) and npm
- `wget` (for downloading `espeak-ng-data` if not already present from Docker build)
- `pip` for Python 3 (Python package manager). If not installed, on Debian/Ubuntu systems, you can install it with: `sudo apt update && sudo apt install python3-pip`

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

    _Note: The `venv` can be created inside the `backend/` directory or the project root. Adjust paths accordingly._

3.  **Install backend dependencies:**
    Ensure `backend/requirements.txt` includes `fastapi`, `uvicorn[standard]`, `python-multipart`, `soundfile`, `sherpa-onnx`, and `huggingface_hub`.

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
    - The API endpoints at `http://localhost:8000/api/...`
    - The interactive API documentation (Swagger UI) at `http://localhost:8000/docs`.

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

## Docker Architecture

When running with Docker, the application uses a multi-stage build process:

1. **Frontend Build Stage**: Builds the Vue.js application using Node.js
2. **Production Stage**:
   - Sets up Python environment with FastAPI backend
   - Copies the built frontend assets to `/app/static`
   - Configures FastAPI to serve both API endpoints and the frontend
   - The backend serves the frontend at the root path (`/`) while API endpoints are available at `/api/*`

## Development vs Production

- **Development**: Backend and frontend run separately (typically on ports 8000 and 5173)
- **Docker/Production**: Single container serves both frontend and backend on port 8000

## Troubleshooting

**Docker Issues:**

- If the build fails, try clearing Docker cache: `docker system prune -a`
- Check logs: `docker-compose logs tts-app`
- For memory issues, ensure Docker has at least 4GB RAM allocated

**Application Issues:**

- If models fail to download, check internet connection and disk space
- For permission issues, ensure the Docker user has proper access to mounted volumes
