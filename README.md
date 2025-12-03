# Introduction

A Mandarin pitch detector for audio.

![tones](./backend/data/output.png)

# Start the Backend Server

The backend is built with FastAPI and handles audio analysis.

Navigate to the `backend/` directory and run the server:

`poetry run uvicorn mandarin_pitch_detector.rest.rest_api:app --reload`

The API will be available at `http://127.0.0.1:8000`.

# Start the Frontend Application

The frontend is a React app built with Vite.

Navigate to the `frontend/` directory and start the development server:

`npm run dev`

The app will be available at `http://localhost:5173`.

# Prerequisites
- Python `v3.12.11`
- poetry `v2.1.3`
- Node.js
- npm

## Backend Environment Setup
The required environment can be installed via poetry, which automatically create a virtual environment under the `./backend/.venv` folder with all required python dependencies.

To create the environment, navigate to the `backend/` directory and run:

`poetry install`

## Frontend Environment Setup

To install dependencies, navigate to the `frontend/` directory and run:

`npm install`