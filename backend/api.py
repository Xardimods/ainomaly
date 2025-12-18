from fastapi import FastAPI, Response
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import uvicorn
import os
import psutil
import cv2
import threading
import json
import glob
from datetime import datetime
import time

app = FastAPI()

# Allow CORS for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables
from camera_manager import RTSPStream
from source.vision.pose_service import PoseService

# Global variables
active_cameras = {} # {id: RTSPStream}
pose_services = {} # {id: PoseService}
SETTINGS_FILE = "settings.json"
CAMERAS_FILE = "cameras.json"
RECORDINGS_DIR = "recordings"

# ... (rest of setup) ...

def get_camera_config(camera_id: str):
    if os.path.exists(CAMERAS_FILE):
        with open(CAMERAS_FILE, 'r') as f:
            cameras = json.load(f)
            for cam in cameras:
                if str(cam["id"]) == str(camera_id):
                    return cam
    return None

def generate_frames(camera_id: str):
    global active_cameras
    
    # Initialize camera if not valid
    if camera_id not in active_cameras or not active_cameras[camera_id].running:
        config = get_camera_config(camera_id)
        if not config:
            return 
            
        src = config["source"]
        
        # Check if enabled
        if not config.get("enabled", True):
             # If disabled, yield blank or just return to close stream
             return

        # Handle Integer indices for webcams vs Strings for RTSP
        if isinstance(src, str) and src.isdigit():
            src = int(src)
            
        # Create and start threaded stream manager
        stream = RTSPStream(src, name=f"Cam_{camera_id}")
        stream.start()
        active_cameras[camera_id] = stream
    
    stream_manager = active_cameras[camera_id]
    
    while True:
        # Check enabled status again in loop (though stream closed by toggle usually)
        if not stream_manager.running:
             break

        # Get latest frame from thread buffer
        success, frame = stream_manager.read()
        
        if not success:
            # If manager is reconnecting or failed, yield a placeholder blank frame
            # rather than breaking, so the HTTP stream stays alive for the browser
            
            # Create a black blank frame 640x360
            import numpy as np
            blank_frame = np.zeros((360, 640, 3), np.uint8)
            ret, buffer = cv2.imencode('.jpg', blank_frame)
            if ret:
                frame_bytes = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
            
            time.sleep(1.0) # Slow update for placeholder
            continue
            
        # Process frame with Vision System
        if camera_id not in pose_services:
            pose_services[camera_id] = PoseService()
        
        frame = pose_services[camera_id].process_frame(frame)
            
        ret, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.get("/video_feed")
def video_feed(id: str):
    print(f"DEBUG: video_feed requested for ID: {id}")
    return StreamingResponse(generate_frames(id), media_type="multipart/x-mixed-replace; boundary=frame")

# --- Camera Management Endpoints ---

@app.post("/cameras/test")
def test_camera_connection(config: dict):
    # Construct URL if it's RTSP structure
    source = config.get("source")
    if config.get("type") == "rtsp":
        # Use helper from class or inline construction
        user = config.get("user", "")
        password = config.get("password", "")
        ip = config.get("ip", "")
        port = config.get("port", "554")
        path = config.get("path", "")
        auth = f"{user}:{password}@" if user and password else ""
        source = f"rtsp://{auth}{ip}:{port}{path}"
        
    print(f"Testing connection to: {source}")
    success = RTSPStream.test_connection(source)
    return {"success": success, "url": source}

@app.get("/cameras")
def get_cameras():
    if os.path.exists(CAMERAS_FILE):
        with open(CAMERAS_FILE, 'r') as f:
            return json.load(f)
    return []

@app.post("/cameras")
def add_camera(camera: dict):
    cameras = []
    if os.path.exists(CAMERAS_FILE):
        with open(CAMERAS_FILE, 'r') as f:
            cameras = json.load(f)
    
    # Generate ID
    new_id = str(len(cameras) + 1)
    if cameras:
        new_id = str(max([int(c["id"]) for c in cameras]) + 1)
    
    # Process Source
    final_source = camera.get("source")
    # If type is RTSP and we received structured fields, build the URL
    if camera.get("type") == "rtsp":
        user = camera.get("user", "")
        password = camera.get("password", "")
        ip = camera.get("ip", "")
        port = camera.get("port", "554")
        path = camera.get("path", "")
        auth = f"{user}:{password}@" if user and password else ""
        final_source = f"rtsp://{auth}{ip}:{port}{path}"
        
    new_cam = {
        "id": new_id,
        "name": camera.get("name", "Camera " + new_id),
        "source": final_source,
        "type": camera.get("type", "webcam"),
        "enabled": True,
        "config": camera
    }
    
    cameras.append(new_cam)
    
    with open(CAMERAS_FILE, 'w') as f:
        json.dump(cameras, f, indent=4)
        
    return new_cam

@app.post("/cameras/{camera_id}/toggle")
def toggle_camera(camera_id: str):
    if os.path.exists(CAMERAS_FILE):
        with open(CAMERAS_FILE, 'r') as f:
            cameras = json.load(f)
            
        new_status = False
        for cam in cameras:
            if str(cam["id"]) == str(camera_id):
                cam["enabled"] = not cam.get("enabled", True)
                new_status = cam["enabled"]
                break
        
        with open(CAMERAS_FILE, 'w') as f:
            json.dump(cameras, f, indent=4)
            
        # If disabled, force stop the stream
        if not new_status and camera_id in active_cameras:
            active_cameras[camera_id].stop()
            active_cameras[camera_id].stop()
            del active_cameras[camera_id]
        
        # Cleanup vision service
        if camera_id in pose_services:
            pose_services[camera_id].close()
            del pose_services[camera_id]
            
        return {"status": "toggled", "enabled": new_status}
    return {"error": "Camera not found"}

@app.delete("/cameras/{camera_id}")
def delete_camera(camera_id: str):
    if os.path.exists(CAMERAS_FILE):
        with open(CAMERAS_FILE, 'r') as f:
            cameras = json.load(f)
            
        cameras = [c for c in cameras if str(c["id"]) != str(camera_id)]
        
        with open(CAMERAS_FILE, 'w') as f:
            json.dump(cameras, f, indent=4)
            
        # Stop stream if active
        if camera_id in active_cameras:
            active_cameras[camera_id].stop()
            active_cameras[camera_id].stop()
            del active_cameras[camera_id]
            
        # Cleanup vision service
        if camera_id in pose_services:
            pose_services[camera_id].close()
            del pose_services[camera_id]
            
    return {"status": "deleted"}

@app.get("/recordings")
def get_recordings():
    files = glob.glob(os.path.join(RECORDINGS_DIR, "*.mp4"))
    data = []
    for i, f in enumerate(files):
        stats = os.stat(f)
        size_mb = round(stats.st_size / (1024 * 1024), 2)
        created = datetime.fromtimestamp(stats.st_ctime).strftime('%Y-%m-%d %H:%M')
        name = os.path.basename(f)
        data.append({
            "id": i,
            "name": name,
            "date": created,
            "size": f"{size_mb} MB"
        })
    return data

@app.get("/settings")
def get_settings():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, 'r') as f:
            return json.load(f)
    return {}

@app.post("/settings")
def update_settings(settings: dict):
    with open(SETTINGS_FILE, 'w') as f:
        json.dump(settings, f, indent=4)
    return {"status": "saved"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8001)
