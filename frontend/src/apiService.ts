import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api'; // Backend running on port 8000

interface TTSInfo {
    // Define based on what useful info you might want from backend beyond audio
    // For now, the backend POST /api/tts only returns the audio file directly.
    // If you modify backend to return JSON with audio URL and info, update this.
    duration?: number;
    processingTime?: number;
    rtf?: number;
}

interface DocumentProcessResponse {
    text: string;         // Preview of processed text
    chunks: string[];    // Text chunks for TTS processing
    filename: string;    // Original filename
    file_type: string;   // File type (pdf, docx, etc.)
}

export const getLanguages = async (): Promise<string[]> => {
    try {
        const response = await axios.get<string[]>(`${API_BASE_URL}/languages`);
        return response.data;
    } catch (error) {
        console.error('Error fetching languages:', error);
        throw error;
    }
};

export const getModelsForLanguage = async (language: string): Promise<string[]> => {
    try {
        const response = await axios.get<string[]>(`${API_BASE_URL}/models/${encodeURIComponent(language)}`);
        return response.data;
    } catch (error) {
        console.error(`Error fetching models for ${language}:`, error);
        throw error;
    }
};

export const submitTTSRequest = async (
    language: string,
    repo_id: string, // model_id
    text: string,
    sid: string, // speaker_id
    speed: number
): Promise<{ audioBlob: Blob; info?: TTSInfo }> => {
    try {
        const response = await axios.post(
            `${API_BASE_URL}/tts`,
            {
                language,
                repo_id,
                text,
                sid,
                speed,
            },
            {
                responseType: 'blob', // Important for receiving audio file
            }
        );
        // If backend sends info in headers, extract it here. e.g., response.headers['x-tts-info']
        // For now, info is not explicitly returned with the audio blob from the current backend.
        return { audioBlob: response.data }; 
    } catch (error) {
        console.error('Error submitting TTS request:', error);
        // Try to parse error response if it's JSON (e.g., for HTTPException details)
        if (axios.isAxiosError(error) && error.response && error.response.data instanceof Blob) {
            const errorBlob = error.response.data;
            const errorText = await errorBlob.text();
            try {
                const errorJson = JSON.parse(errorText);
                throw new Error(errorJson.detail || 'TTS API request failed');
            } catch (parseError) {
                throw new Error(errorText || 'TTS API request failed and error response was not valid JSON');
            }
        }
        throw error;
    }
};

/**
 * Process a document file and extract text for TTS
 * @param file Document file (PDF, DOCX, PPTX, TXT)
 * @param maxChunkLength Maximum length of each text chunk
 * @returns Processed document response with text chunks
 */
export const processDocument = async (
    file: File,
    maxChunkLength: number = 5000
): Promise<DocumentProcessResponse> => {
    try {
        const formData = new FormData();
        formData.append('file', file);
        formData.append('max_chunk_length', maxChunkLength.toString());
        
        const response = await axios.post<DocumentProcessResponse>(
            `${API_BASE_URL}/process-document`,
            formData,
            {
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
            }
        );
        
        return response.data;
    } catch (error) {
        console.error('Error processing document:', error);
        if (axios.isAxiosError(error) && error.response) {
            const errorData = error.response.data;
            if (typeof errorData === 'object' && errorData.detail) {
                throw new Error(errorData.detail);
            }
        }
        throw error;
    }
};

/**
 * Generate TTS audio from a document text chunk
 * @param language Selected language
 * @param repoId Model ID
 * @param textChunk Text chunk to process
 * @param sid Speaker ID
 * @param speed Speech speed
 * @returns Audio blob
 */
export const generateTTSFromChunk = async (
    language: string,
    repoId: string,
    textChunk: string,
    sid: string,
    speed: number
): Promise<Blob> => {
    try {
        const formData = new FormData();
        formData.append('language', language);
        formData.append('repo_id', repoId);
        formData.append('text_chunk', textChunk);
        formData.append('sid', sid);
        formData.append('speed', speed.toString());
        
        const response = await axios.post(
            `${API_BASE_URL}/tts-from-chunk`,
            formData,
            {
                responseType: 'blob'
            }
        );
        
        return response.data;
    } catch (error) {
        console.error('Error generating TTS from chunk:', error);
        if (axios.isAxiosError(error) && error.response && error.response.data instanceof Blob) {
            const errorBlob = error.response.data;
            const errorText = await errorBlob.text();
            try {
                const errorJson = JSON.parse(errorText);
                throw new Error(errorJson.detail || 'TTS chunk processing failed');
            } catch (parseError) {
                throw new Error(errorText || 'TTS chunk processing failed');
            }
        }
        throw error;
    }
};
