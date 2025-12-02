from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import tempfile
import shutil
from mandarin_pitch_detector.pitch_detector import praat_pitch_detector

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
    try:
        with tempfile.NamedTemporaryFile(delete=True) as tmp:
            shutil.copyfileobj(audio.file, tmp)
            wav_path = tmp.name

            result = praat_pitch_detector(wav_path)
            return JSONResponse(content=result)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
