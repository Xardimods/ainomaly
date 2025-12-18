from ultralytics import YOLO
import cv2
import numpy as np
import time

# Use relative imports assuming this is run as part of the backend package
try:
    from .fall_detector import FallDetector
    from .chatbot import on_event
except ImportError:
    # Fallback for direct execution
    from fall_detector import FallDetector
    from chatbot import on_event

class PoseService:
    def __init__(self, camera_id="1", alert_manager=None):
        self.camera_id = camera_id
        self.alert_manager = alert_manager
        self.disabled = False
        self.detector = FallDetector()
        self.model = None
        
        # Caching for performance
        self.last_inference_time = 0
        self.inference_interval = 0.1 # Run AI every 100ms (10 FPS)
        self.last_results = None
        self.last_posture = "Desconocido"
        
        try:
            print(f"[PoseService] Initializing YOLOv8n-pose for Cam {camera_id}...")
            # Load nano model for speed
            self.model = YOLO('yolov8n-pose.pt') 
            print(f"[PoseService] YOLOv8n-pose initialized for Cam {camera_id}.")
        except Exception as e:
            print(f"[PoseService] WARNING: Vision system disabled. Error: {e}")
            self.disabled = True

    def process_frame(self, frame):
        if self.disabled or frame is None or self.model is None:
            return frame

        try:
            current_time = time.time()
            
            # --- INFERENCE THROTTLING ---
            # Only run heavy model inference if enough time has passed
            if current_time - self.last_inference_time > self.inference_interval:
                # Run Inference
                results = self.model(frame, verbose=False, conf=0.5)
                self.last_results = results
                self.last_inference_time = current_time
                
                # Analyze posture from valid results
                for result in results:
                    if result.keypoints is not None and result.keypoints.xyn.shape[1] >= 17:
                        kpts = result.keypoints.xyn[0] 
                        
                        def get_p(idx):
                            return (float(kpts[idx][0]), float(kpts[idx][1]))

                        coords = {
                            "left_shoulder": get_p(5), "right_shoulder": get_p(6),
                            "left_hip": get_p(11), "right_hip": get_p(12),
                            "left_knee": get_p(13), "right_knee": get_p(14),
                            "left_ankle": get_p(15), "right_ankle": get_p(16)
                        }

                        posture, event = self.detector.classify_posture(coords)
                        self.last_posture = posture
                        
                        if event:
                            on_event(event, posture)
                        
                        # Continuous monitoring for AlertManager
                        if self.alert_manager:
                            alert_status = "Caída detectada" if posture == "Caido" else "Normal"
                            self.alert_manager.process_event(
                                self.camera_id, 
                                f"Cámara {self.camera_id}", 
                                alert_status, 
                                0.90, 
                                frame
                            )
                        break

            # --- DRAWING (Always draw using cached results) ---
            
            # Draw Skeleton (if we have results)
            if self.last_results:
                for result in self.last_results:
                     # We use the built-in plotter on the CURRENT frame
                     # Note: result.plot() creates a new image. We want to draw on 'frame'.
                     # Actually, result.plot() returns the image. 
                     # Optimally we should just draw manually if caching, 
                     # but detection boxes might drift if camera moves fast.
                     # For simplicity/robustness, we re-plot the *old* detection on the *new* frame? 
                     # No, that looks floaty. 
                     # Better approach: Just draw the overlay if inference ran?
                     # No, user wants smooth 30fps video with 10fps AI.
                     # If we don't draw anything in between, the skeleton flickers.
                     # YOLO's result.plot() creates a new numpy array.
                     
                     # To avoid flicker, we can't easily use result.plot() on a *different* frame 
                     # because 'result' contains specific image dimensions/data.
                     # So we only update the 'frame' with the plot output WHEN we run inference.
                     # But for the skipped frames, we just return the raw frame with TEXT overlay.
                     # Skeleton overlay will effectively run at 10fps (jittery) on top of 30fps video?
                     # Or we can just accept 30fps inference if YOLOv8n is fast enough (it usually is >50fps on CPU).
                     # The user's issue was "slow RTSP". That was because I BLOCKED the Capture thread.
                     # Moving it back to API thread decouples it naturally.
                     # API thread can run as slow as it wants (15fps) while RTSP capture is 30fps.
                     
                     # Let's simple-draw:
                     # If inference ran, we replace 'frame' with plotted version.
                     # If skipped, we return raw frame.
                     # Result: Stuttery skeleton, smooth video. This is acceptable.
                     pass

            # Update 'frame' if we just ran inference? 
            # Actually, YOLO plot() returns a NEW image.
            # If we are in skipping mode, we haven't updated 'frame'.
            
            if self.last_results:
                 # Re-draw the cached result on the current frame?
                 # result.plot(img=frame) allows drawing on custom image! (Ultralytics feature)
                 for result in self.last_results:
                     frame = result.plot(img=frame)
                     break

            # Draw Status Text (Always, using cached posture)
            posture = self.last_posture
            
            # Colors (BGR) matching Tailwind
            colors = {
                "De pie": (129, 185, 16),    # Emerald-500
                "Sentado": (235, 96, 59),    # Blue-500
                "Caido": (87, 67, 244),      # Rose-500
                "Agachado": (235, 96, 59),   # Blue-500
                "Desconocido": (148, 163, 184) # Slate-400
            }
            
            text_color = (255, 255, 255) # White text
            bg_color = colors.get(posture, (148, 163, 184))
            
            # Text Config
            font = cv2.FONT_HERSHEY_DUPLEX
            font_scale = 1.0
            thickness = 1
            padding = 10
            
            (text_w, text_h), baseline = cv2.getTextSize(posture, font, font_scale, thickness)
            x, y = 30, 80
            
            cv2.rectangle(frame, 
                         (x - padding, y - text_h - padding), 
                         (x + text_w + padding, y + padding), 
                         bg_color, -1) 
            
            cv2.putText(frame, posture, (x, y),
                        font, font_scale, text_color, thickness, cv2.LINE_AA)

        except Exception as e:
            # print(f"[PoseService] Error processing frame: {e}")
            pass
            
        return frame

    def close(self):
        # Nothing specific to close for YOLO
        pass
