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
    def __init__(self):
        self.disabled = False
        self.detector = FallDetector()
        self.model = None
        
        try:
            print("[PoseService] Initializing YOLOv8n-pose...")
            # Load nano model for speed
            self.model = YOLO('yolov8n-pose.pt') 
            print("[PoseService] YOLOv8n-pose initialized.")
        except Exception as e:
            print(f"[PoseService] WARNING: Vision system disabled. Error: {e}")
            self.disabled = True

    def process_frame(self, frame):
        if self.disabled or frame is None or self.model is None:
            return frame

        try:
            # YOLO expects BGR, so no conversion needed if input is BGR.
            # verbose=False to reduce console spam
            results = self.model(frame, verbose=False, conf=0.5)
            
            posture = "Desconocido"
            
            # Process first detection
            for result in results:
                # Keypoints: (1, 17, 3) tensor [x, y, conf], normalized if we access .xyn
                if result.keypoints is not None and result.keypoints.xyn.shape[1] >= 17:
                    # Get normalized keypoints (x, y)
                    kpts = result.keypoints.xyn[0] # First person
                    
                    # YOLO Keypoint Mapping COCO
                    # 5: Left Shoulder, 6: Right Shoulder
                    # 11: Left Hip, 12: Right Hip
                    # 13: Left Knee, 14: Right Knee
                    # 15: Left Ankle, 16: Right Ankle
                    
                    def get_p(idx):
                        # tensor to float tuple
                        return (float(kpts[idx][0]), float(kpts[idx][1]))

                    # Check visibility/confidence if needed, but for now just pass coords
                    # If x,y are 0,0 it implies not detected
                    
                    coords = {
                        "left_shoulder": get_p(5),
                        "right_shoulder": get_p(6),
                        "left_hip": get_p(11),
                        "right_hip": get_p(12),
                        "left_knee": get_p(13),
                        "right_knee": get_p(14),
                        "left_ankle": get_p(15),
                        "right_ankle": get_p(16)
                    }

                    posture, event = self.detector.classify_posture(coords)
                    
                    if event:
                        on_event(event, posture)

                    # Draw Overlay
                    # YOLO has a built-in plotter: result.plot()
                    # It returns a BGR numpy array with boxes and keypoints
                    frame = result.plot() 
                    
                    break # Single person tracking for now

            # --- Draw Styling ---
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
            
            # Calculate text size
            (text_w, text_h), baseline = cv2.getTextSize(posture, font, font_scale, thickness)
            
            # Position (Top-Left corner)
            x, y = 30, 80
            
            # Draw Badge Background (Rounded rect simulation with filled rectangle)
            # Main box
            cv2.rectangle(frame, 
                         (x - padding, y - text_h - padding), 
                         (x + text_w + padding, y + padding), 
                         bg_color, 
                         -1) # Filled
            
            # Draw Text
            cv2.putText(frame, posture, (x, y),
                        font, font_scale, text_color, thickness, cv2.LINE_AA)

                        
        except Exception as e:
            # print(f"[PoseService] Error processing frame: {e}")
            pass
            
        return frame

    def close(self):
        # Nothing specific to close for YOLO
        pass
