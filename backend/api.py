from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os

app = FastAPI()

# Allow CORS for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"status": "online", "version": "3.1.0"}

@app.get("/status")
def get_status():
    return {"connected": True, "camera_status": "standby"}

@app.get("/recordings")
def get_recordings():
    # Placeholder: return mock data or list actual files
    return [
        {"id": 1, "name": "recording_001.mp4", "date": "2023-10-27"},
        {"id": 2, "name": "recording_002.mp4", "date": "2023-10-28"},
    ]

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8001)
