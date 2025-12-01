from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import tempfile
import os
import shutil
from mandarin_pitch_detector.pitch_detector import praat_pitch_detector
import subprocess

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analyze_tone_praat")
async def analyze_tone(audio: UploadFile = File(...)):
    # Create a single temp WAV file and write the audio data
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_wav:
        print("Content type:", audio.content_type)
        print("Filename:", audio.filename)
        print("Size:", audio.file.__sizeof__())
        print("file path:", tmp_wav.name)
        shutil.copyfileobj(audio.file, tmp_wav)
        wav_path = tmp_wav.name
    
    try:
        # Analyze the converted WAV file
        result = praat_pitch_detector(wav_path)
        return JSONResponse(content=result)
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=400, detail=f"Audio conversion failed: {e.stderr.decode()}")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # Clean up the temp file
        if os.path.exists(wav_path):
            os.remove(wav_path)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
