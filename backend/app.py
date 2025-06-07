#!/usr/bin/env python3
#
# Copyright      2022-2023  Xiaomi Corp.        (authors: Fangjun Kuang)
#
# See LICENSE for clarification regarding multiple authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import time
import uuid
import base64
from datetime import datetime
from typing import List, Dict, Any, Optional

import soundfile as sf
import uvicorn
from fastapi import FastAPI, HTTPException, Body, File, UploadFile, Form
from fastapi.responses import FileResponse, RedirectResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

# Importações absolutas para funcionar com o uvicorn diretamente
try:
    from backend.model import get_pretrained_model, language_to_models
    from backend.document_processor import DocumentProcessor
except ImportError:
    # Fallback para execução direta do diretório backend
    from model import get_pretrained_model, language_to_models
    from document_processor import DocumentProcessor

# FastAPI app instance
app = FastAPI(title="Next-gen Kaldi: Text-to-speech (TTS) API")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173", "http://127.0.0.1:5173",  # Vite dev server
        "http://localhost:3000", "http://127.0.0.1:3000",  # Alternative dev server
        "http://localhost:8080", "http://127.0.0.1:8080",  # Vue CLI dev server
        "http://localhost", "http://127.0.0.1",  # General localhost
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["Content-Disposition"],
    max_age=600  # Cache preflight requests for 10 minutes
)

@app.get("/", include_in_schema=False)
async def root_redirect():
    return RedirectResponse(url="/docs")

def MyPrint(s):
    now = datetime.now()
    date_time = now.strftime("%Y-%m-%d %H:%M:%S.%f")
    print(f"{date_time}: {s}")

# This is the core TTS processing function, used by the FastAPI endpoint
def do_tts_processing(language: str, repo_id: str, text: str, sid_str: str, speed: float):
    MyPrint(f"Language: {language}")
    MyPrint(f"Model ID (repo_id): {repo_id}")
    MyPrint(f"Text: {text}")
    MyPrint(f"Speaker ID: {sid_str}")
    MyPrint(f"Speed: {speed}")

    if not text.strip():
        MyPrint("Error: Text cannot be empty.")
        raise ValueError("Text cannot be empty or contain only spaces.")

    expected_fields = language_to_models[language][repo_id]

    extra_col_name = None
    if "speaker_id_col" in expected_fields:
        extra_col_name = expected_fields["speaker_id_col"]
        MyPrint(f"Speaker ID column: {extra_col_name}")

    sid = None
    if extra_col_name is not None:
        if sid_str.strip() == "":
            MyPrint(f"Warning: No speaker ID provided for a multi-speaker model. Defaulting to 0 or first available.")
            # Default to 0 or handle as needed, model might pick a default or error
            # For now, let's try to pass sid as None if not provided, model loader might handle it.
            # Or, if the model strictly requires an int, default to 0.
            try:
                # Attempt to get the first available speaker ID if not provided
                if hasattr(get_pretrained_model, 'get_speaker_ids') and callable(getattr(get_pretrained_model, 'get_speaker_ids')):
                    available_sids = get_pretrained_model.get_speaker_ids(repo_id)
                    if available_sids:
                        sid = available_sids[0] # Use the first available ID
                        MyPrint(f"Defaulting to first available speaker ID: {sid}")
                    else:
                         sid = 0 # Fallback if no specific default mechanism
                         MyPrint(f"Could not determine available speaker IDs, defaulting speaker ID to 0.")
                else:
                    sid = 0 # Fallback if no specific default mechanism
                    MyPrint(f"Speaker ID detection method not available, defaulting speaker ID to 0.")
            except Exception as e_sid:
                MyPrint(f"Error determining default speaker ID, defaulting to 0: {e_sid}")
                sid = 0
        else:
            try:
                sid = int(sid_str)
                MyPrint(f"Using provided speaker ID: {sid}")
            except ValueError:
                MyPrint(
                    f'Invalid speaker ID: {sid_str}. Please input an integer for speaker ID.'
                )
                raise ValueError(f'Invalid speaker ID: {sid_str}. Must be an integer.')
    else:
        MyPrint("This is a single-speaker model. Speaker ID is not used.")

    tts_model = get_pretrained_model(repo_id=repo_id, speed=speed)
    MyPrint(f"model.py: {tts_model}")

    try:
        waves = tts_model.generate_with_text(text=text, sid=sid, speed=speed).samples
    except Exception as e:
        MyPrint(f"Error during TTS generation: {e}")
        # Provide a more user-friendly error if possible, or re-raise
        raise RuntimeError(f"Failed to generate audio: {str(e)}")

    sample_rate = tts_model.sample_rate
    # Save the generated audio to a temporary file
    # Using a unique filename for each request to avoid conflicts
    output_dir = "/tmp/tts_audio_cache"
    os.makedirs(output_dir, exist_ok=True)
    filename = os.path.join(output_dir, f"tts_output_{uuid.uuid4().hex}.wav")
    
    sf.write(filename, waves, samplerate=sample_rate)
    MyPrint(f"Generated audio saved to: {filename}")

    info = f"Generated successfully! Language: {language}, Model: {repo_id}, Speaker ID: {sid}, Speed: {speed}"
    return filename, info

def download_espeak_ng_data():
    espeak_data_dir = "/tmp/espeak-ng-data"
    if not os.path.exists(os.path.join(espeak_data_dir, "espeak-ng-data", "phontab")):
        MyPrint("Downloading espeak-ng-data...")
        os.makedirs(espeak_data_dir, exist_ok=True)
        cmd = f"cd {espeak_data_dir} && " \
              f"wget -qO- https://github.com/k2-fsa/sherpa-onnx/releases/download/tts-models/espeak-ng-data.tar.bz2 | tar -xj --strip-components=1"
        ret_code = os.system(cmd)
        if ret_code == 0:
            MyPrint("espeak-ng-data downloaded and extracted successfully.")
            os.environ["ESPEAK_DATA_PATH"] = espeak_data_dir
        else:
            MyPrint(f"Error downloading/extracting espeak-ng-data. wget/tar returned {ret_code}")
    else:
        MyPrint("espeak-ng-data already exists.")
        os.environ["ESPEAK_DATA_PATH"] = espeak_data_dir

# --- FastAPI Endpoints ---
@app.get("/api/languages", summary="Get Available Languages")
def get_languages_endpoint() -> List[str]: # Renamed to avoid conflict if imported
    return list(language_to_models.keys())

@app.get("/api/models/{language}", summary="Get Available Models for a Language")
def get_models_for_language_endpoint(language: str) -> List[str]: # Renamed
    if language in language_to_models:
        return language_to_models[language]
    raise HTTPException(status_code=404, detail="Language not found")

class TTSRequest(BaseModel):
    language: str
    repo_id: str # Model ID
    text: str
    sid: str # Speaker ID (can be string initially, converted to int in processing)
    speed: float

class DocumentProcessResponse(BaseModel):
    text: str
    chunks: List[str] = Field(default_factory=list)
    filename: str
    file_type: str

@app.post("/api/tts", summary="Generate Text-to-Speech Audio")
async def text_to_speech_api(request: TTSRequest = Body(...)):
    try:
        filename, info = do_tts_processing(
            request.language,
            request.repo_id,
            request.text,
            request.sid, # Pass sid as string, do_tts_processing will handle conversion/defaulting
            request.speed
        )
        return FileResponse(path=filename, media_type='audio/wav', filename=os.path.basename(filename))
    except ValueError as ve:
        MyPrint(f"TTS API Value Error: {ve}")
        raise HTTPException(status_code=400, detail=str(ve))
    except RuntimeError as re:
        MyPrint(f"TTS API Runtime Error: {re}")
        raise HTTPException(status_code=500, detail=str(re)) 
    except Exception as e:
        MyPrint(f"TTS API Unexpected Error: {e}")
        raise HTTPException(status_code=500, detail=f"An internal error occurred: {str(e)}")

@app.post("/api/process-document", summary="Process document and extract text for TTS")
async def process_document_api(
    file: UploadFile = File(...),
    max_chunk_length: Optional[int] = Form(5000)
):
    try:
        # Read file content
        file_content = await file.read()
        filename = file.filename
        file_type = os.path.splitext(filename)[1].lower().replace('.', '')
        
        MyPrint(f"Processing document: {filename}, type: {file_type}")
        
        # Process document based on file type
        text = DocumentProcessor.process_document(file_content, filename)
        
        # Format and chunk text for TTS
        chunks = DocumentProcessor.format_text_for_tts(text, max_chunk_length)
        
        MyPrint(f"Document processed successfully. Extracted {len(chunks)} text chunks.")
        
        return DocumentProcessResponse(
            text=text[:1000] + "..." if len(text) > 1000 else text,  # Preview of text
            chunks=chunks,
            filename=filename,
            file_type=file_type
        )
    except ValueError as ve:
        MyPrint(f"Document Processing Error: {ve}")
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        MyPrint(f"Document Processing Unexpected Error: {e}")
        raise HTTPException(status_code=500, detail=f"An error occurred during document processing: {str(e)}")

@app.post("/api/tts-from-chunk", summary="Generate TTS from a document text chunk")
async def tts_from_chunk_api(
    language: str = Form(...),
    repo_id: str = Form(...),
    text_chunk: str = Form(...),
    sid: str = Form("0"),
    speed: float = Form(1.0)
):
    try:
        filename, info = do_tts_processing(
            language,
            repo_id,
            text_chunk,
            sid,
            speed
        )
        return FileResponse(path=filename, media_type='audio/wav', filename=os.path.basename(filename))
    except ValueError as ve:
        MyPrint(f"TTS Chunk API Value Error: {ve}")
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        MyPrint(f"TTS Chunk API Error: {e}")
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

if __name__ == "__main__":
    download_espeak_ng_data()
    MyPrint("Starting FastAPI server with Uvicorn...")
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
