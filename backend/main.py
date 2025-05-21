from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
import os
from model import get_pretrained_model, language_to_models
import soundfile as sf
import uuid
from datetime import datetime
import asyncio
from fastapi.responses import FileResponse
import PyPDF2
from docx import Document

app = FastAPI(title="Advanced TTS API")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Models
class TTSRequest(BaseModel):
    language: str
    model_id: str
    text: str
    speaker_id: int = 0
    speed: float = 1.0

class DocumentConversionRequest(BaseModel):
    file_path: str
    language: str
    model_id: str
    speaker_id: int = 0
    speed: float = 1.0

# TTS endpoints
@app.post("/api/tts")
async def text_to_speech(request: TTSRequest):
    try:
        model = get_pretrained_model(request.model_id)
        audio_path = f"{uuid.uuid4()}.wav"
        
        # Generate audio
        audio = model.generate(
            request.text,
            speaker=request.speaker_id,
            speed=request.speed
        )
        
        sf.write(audio_path, audio, model.sample_rate)
        return {"audio_path": audio_path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/upload-document")
async def upload_document(file: UploadFile = File(...)):
    try:
        file_path = f"uploads/{file.filename}"
        os.makedirs("uploads", exist_ok=True)
        
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        return {"file_path": file_path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/models/{language}")
async def get_models(language: str):
    try:
        models = language_to_models.get(language, [])
        return {"models": models}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/audio/{filename}")
async def get_audio(filename: str):
    try:
        return FileResponse(filename)
    except Exception as e:
        raise HTTPException(status_code=404, detail="Audio file not found")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
