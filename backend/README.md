# Testupavois - Advanced Text-to-Speech API

Testupavois is a powerful Text-to-Speech (TTS) API built with FastAPI that supports multiple languages and various document formats. The system utilizes state-of-the-art TTS models and provides a flexible, scalable solution for converting text to speech.

## Features

- Multi-language support with multiple TTS models per language
- Document processing for various formats (PDF, DOCX, PPTX, TXT)
- Real-time text-to-speech conversion
- Customizable speech parameters (speed, speaker selection)
- CORS-enabled API for web integration
- Support for both single-speaker and multi-speaker models
- Efficient audio file handling and delivery

## Technologies Used

- **FastAPI**: Modern, fast web framework for building APIs
- **Python 3.x**: Core programming language
- **sherpa-onnx**: TTS model handling and generation
- **PyPDF2**: PDF document processing
- **python-docx**: DOCX document processing
- **python-pptx**: PowerPoint presentation processing
- **soundfile**: Audio file handling
- **uvicorn**: ASGI server implementation

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd Testupavois/backend
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the server:
```bash
python main.py
```

The server will start at `http://localhost:8000`

## API Endpoints

### Text to Speech
- `POST /api/tts`
  - Convert text to speech
  - Request body: `TTSRequest`
  ```json
  {
    "language": "string",
    "model_id": "string",
    "text": "string",
    "speaker_id": 0,
    "speed": 1.0
  }
  ```

### Document Upload
- `POST /api/upload-document`
  - Upload document for processing
  - Accepts multipart/form-data

### Model Information
- `GET /api/models/{language}`
  - Get available models for a specific language

### Audio Retrieval
- `GET /api/audio/{filename}`
  - Retrieve generated audio file

## Supported Languages

The system supports a wide range of languages including but not limited to:
- English
- Chinese (Mandarin and Cantonese)
- German
- French
- Spanish
- Russian
- Japanese
- And many more (40+ languages)

## Document Processing

The system can process various document formats:
- PDF files
- Microsoft Word documents (DOCX)
- PowerPoint presentations (PPTX)
- Plain text files (TXT)

## Development Backlog

### Priority 1 - Core Features
- [ ] Implement batch processing for multiple text segments
- [ ] Add audio format conversion options (WAV, MP3, OGG)
- [ ] Implement caching system for frequently requested audio
- [ ] Add rate limiting and API key authentication

### Priority 2 - Enhanced Features
- [ ] Add text preprocessing options (normalization, cleaning)
- [ ] Implement streaming audio response
- [ ] Add support for more document formats (RTF, EPUB)
- [ ] Create speech parameter presets

### Priority 3 - Optimization
- [ ] Optimize document processing for large files
- [ ] Implement parallel processing for batch requests
- [ ] Add compression options for audio files
- [ ] Optimize model loading and caching

### Priority 4 - Integration & Monitoring
- [ ] Add detailed API usage metrics
- [ ] Implement webhook notifications
- [ ] Create integration examples for common frameworks
- [ ] Add health check endpoints

## Error Handling

The API implements comprehensive error handling for:
- Invalid request parameters
- Unsupported file formats
- Model loading issues
- File processing errors
- Audio generation failures

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License

This project is licensed under the Apache License 2.0 - see the LICENSE file for details.

## Acknowledgments

- Thanks to the sherpa-onnx project for TTS model support
- Special thanks to the FastAPI community
- Document processing libraries contributors
