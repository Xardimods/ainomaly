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

# Ensure snapshots dir exists for static serving
SNAPSHOTS_DIR = "snapshots"
if not os.path.exists(SNAPSHOTS_DIR):
    os.makedirs(SNAPSHOTS_DIR)

app.mount("/snapshots", StaticFiles(directory=SNAPSHOTS_DIR), name="snapshots")

# Ensure recordings dir exists for static serving
RECORDINGS_DIR = "recordings"
if not os.path.exists(RECORDINGS_DIR):
    os.makedirs(RECORDINGS_DIR)

app.mount("/recordings", StaticFiles(directory=RECORDINGS_DIR), name="recordings")

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
            
        # Process frame with Vision System (Throttled inside PoseService)
        if camera_id not in pose_services:
            pose_services[camera_id] = PoseService(camera_id=camera_id, alert_manager=alert_manager)
        
        try:
            frame = pose_services[camera_id].process_frame(frame)
        except Exception as e:
            print(f"Vision processing error: {e}")
            
        ret, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')


@app.get("/video_feed")
def video_feed(id: str):
    print(f"DEBUG: video_feed requested for ID: {id}")
    return StreamingResponse(generate_frames(id), media_type="multipart/x-mixed-replace; boundary=frame")

import asyncio

@app.get("/events")
async def sse_events():
    async def event_generator():
        while True:
            try:
                while not alert_manager.notification_queue.empty():
                    item = alert_manager.notification_queue.get_nowait()
                    yield f"data: {json.dumps(item)}\n\n"
            except Exception as e:
                print(f"SSE Error: {e}")
            
            await asyncio.sleep(0.5)

    return StreamingResponse(event_generator(), media_type="text/event-stream")

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

    return data

@app.delete("/api/recordings/{filename}")
def delete_recording(filename: str):
    # Security: prevent directory traversal
    filename = os.path.basename(filename) 
    file_path = os.path.join(RECORDINGS_DIR, filename)
    if os.path.exists(file_path):
        try:
            os.remove(file_path)
            return {"status": "deleted"}
        except Exception as e:
            return {"error": f"Error del sistema: {str(e)}"}
    return {"error": "File not found"}

@app.get("/snapshots")
def get_snapshots():
    if not os.path.exists(SNAPSHOTS_DIR):
        return []
    
    files = glob.glob(os.path.join(SNAPSHOTS_DIR, "*.jpg"))
    data = []
    # Sort files by creation time descending
    files.sort(key=os.path.getctime, reverse=True)
    
    for f in files:
        stats = os.stat(f)
        size_kb = round(stats.st_size / 1024, 1)
        created = datetime.fromtimestamp(stats.st_ctime).strftime('%Y-%m-%d %H:%M:%S')
        name = os.path.basename(f)
        
        data.append({
            "name": name,
            "url": f"/snapshots/{name}",
            "date": created,
            "size": f"{size_kb} KB"
        })
    return data

@app.delete("/api/snapshots/{filename}")
def delete_snapshot(filename: str):
    # Security: prevent directory traversal
    filename = os.path.basename(filename) 
    file_path = os.path.join(SNAPSHOTS_DIR, filename)
    if os.path.exists(file_path):
        try:
            os.remove(file_path)
            return {"status": "deleted"}
        except Exception as e:
            return {"error": f"Error del sistema: {str(e)}"}
    return {"error": "File not found"}

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

# --- Alerts Management Endpoints ---
from source.services.alert_manager import AlertManager
alert_manager = AlertManager()

@app.get("/alerts/settings")
def get_alert_settings():
    return alert_manager.get_settings()

@app.post("/alerts/settings")
def update_alert_settings(settings: dict):
    return alert_manager.update_settings(settings)

@app.get("/alerts/history")
def get_alert_history():
    return alert_manager.get_history()

@app.delete("/alerts/history/{alert_id}")
def delete_alert(alert_id: str):
    success = alert_manager.delete_alert(alert_id)
    if success:
        return {"status": "deleted"}
    return {"error": "Alert not found"}, 404

from pydantic import BaseModel
from typing import Optional

class TestAlertConfig(BaseModel):
    telegram_token: Optional[str] = None
    telegram_chat_id: Optional[str] = None

@app.post("/alerts/discover")
def discover_telegram_users(config: TestAlertConfig):
    users = alert_manager.discover_users(token=config.telegram_token)
    return users

@app.post("/alerts/test")
def test_alert_connection(config: TestAlertConfig):
    success, msg, found_id = alert_manager.test_connection(token=config.telegram_token, chat_id=config.telegram_chat_id)
    return {"success": success, "message": msg, "chat_id": found_id}

@app.post("/alerts/test_full")
def test_full_alert():
    # Simulate a fall alert
    alert_manager._trigger_alert("TEST", "Cámara de Prueba", "Caída detectada (SIMULACRO)", 0.99, None)
    return {"status": "triggered"}

import shutil

@app.get("/status")
def get_system_status():
    # System Stats (non-blocking)
    cpu = psutil.cpu_percent(interval=None)
    ram = psutil.virtual_memory().percent
    
    # Camera Status
    active_count = 0
    # Check actual running streams
    for cam_id, stream in active_cameras.items():
        if stream.running:
            active_count += 1
            
    cam_status = f"{active_count} Activas" if active_count > 0 else "Standby"
    
    # Storage Usage (Percentage of partition where . is located)
    # If RECORDINGS_DIR doesn't exist, use current dir
    target_dir = RECORDINGS_DIR if os.path.exists(RECORDINGS_DIR) else "."
    total, used, free = shutil.disk_usage(target_dir)
    storage_percent = round((used / total) * 100, 1)

    return {
        "connected": True,
        "camera_status": cam_status,
        "system": {
            "cpu": cpu,
            "ram": ram
        },
        "storage": {
            "percent": storage_percent,
            "free_gb": round(free / (1024**3), 1)
        }
    }

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8001)
