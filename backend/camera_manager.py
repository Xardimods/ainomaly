import cv2
import threading
import time
import os

class RTSPStream:
    def __init__(self, source, name="Camera"):
        self.source = source
        self.name = name
        self.stream = None
        self.frame = None
        self.running = False
        self.lock = threading.Lock()
        self.thread = None
        self.last_read_time = 0
        
        # Connection status
        self.connected = False
        self.is_reconnecting = False
        
    def construct_url(self, config):
        """
        Helper to build RTSP URL from config dict.
        Expected keys: ip, port, user, password, path
        """
        user = config.get("user", "")
        password = config.get("password", "")
        ip = config.get("ip", "")
        port = config.get("port", "554")
        path = config.get("path", "")
        
        auth = f"{user}:{password}@" if user and password else ""
        url = f"rtsp://{auth}{ip}:{port}{path}"
        return url

    def start(self):
        if self.running:
            return self
            
        self.running = True
        self.thread = threading.Thread(target=self._update, daemon=True)
        self.thread.start()
        return self

    def _update(self):
        retry_delay = 1
        max_retry_delay = 30

        while self.running:
            try:
                if self.stream is None or not self.stream.isOpened():
                    self.connected = False
                    self.is_reconnecting = True
                    
                    # Logic differentiation based on source type
                    # Logic differentiation based on source type
                    if isinstance(self.source, int):
                        # WEBCAM (USB)
                        try:
                            # Suppress excessive OpenCV logging for probing (if available)
                            try:
                                if hasattr(cv2, 'utils') and hasattr(cv2.utils, 'logging'):
                                    cv2.utils.logging.setLogLevel(cv2.utils.logging.LOG_LEVEL_ERROR)
                            except AttributeError:
                                pass # Older OpenCV versions might not have this
                            
                            print(f"[CAM] Connecting to Webcam {self.source}...")
                            
                            # On Windows, try CAP_DSHOW first (faster)
                            if os.name == 'nt':
                                cap = cv2.VideoCapture(self.source, cv2.CAP_DSHOW)
                                # Fallback if DSHOW fails to open or is extremely slow
                                if not cap is None and not cap.isOpened():
                                    print(f"[CAM] DirectShow failed for Webcam {self.source}. Trying Auto...")
                                    cap = cv2.VideoCapture(self.source)
                            else:
                                cap = cv2.VideoCapture(self.source)

                            if cap is None or not cap.isOpened():
                                print(f"[CAM] Error: Camera Index {self.source} not found or occupied.")
                        except Exception as e:
                            print(f"[CAM] Exception opening Webcam {self.source}: {e}")
                            cap = None
                    else:
                        # RTSP / IP STREAM
                        # Force TCP for RTSP stability (prevents UDP packet loss artifacts)
                        os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;tcp"
                        print(f"[RTSP] Connecting to {self.name}...")
                        # Force FFMPEG backend for network streams
                        cap = cv2.VideoCapture(self.source, cv2.CAP_FFMPEG)
                    
                    if cap and cap.isOpened():
                        # Set low buffer size to minimize latency
                        cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
                        self.stream = cap
                        self.connected = True
                        self.is_reconnecting = False
                        self.last_read_time = time.time() # Reset watchdog
                        retry_delay = 1 # Reset off
                        print(f"[CAM] Connected to {self.name}")
                    else:
                        print(f"[CAM] Connection failed to {self.name}. Retrying in {retry_delay}s...")
                        time.sleep(retry_delay)
                        retry_delay = min(retry_delay * 2, max_retry_delay)
                        continue

                if self.connected and (time.time() - self.last_read_time) > 5.0 and self.last_read_time > 0:
                    print(f"[CAM] Watchdog: No frames for 5s from {self.name}. Reconnecting...")
                    self.connected = False
                    if self.stream:
                        self.stream.release()
                    continue

                # Read frame
                ret, frame = self.stream.read()
                
                if ret:
                    # Debug print for first frame or occasionally
                    # print(f"DEBUG: Frame received from {self.name}: {frame.shape}")
                    with self.lock:
                        self.frame = frame
                        self.last_read_time = time.time()
                else:
                    print(f"[CAM] Frame read failed for {self.name} (Ret: {ret}). Reconnecting...")
                    self.connected = False
                    if self.stream:
                        self.stream.release()
                    time.sleep(1) # Brief pause before reconnect loop takes over
                    
            except Exception as e:
                print(f"[CAM] Error in thread for {self.name}: {e}")
                self.connected = False
                if self.stream:
                    self.stream.release()
                time.sleep(retry_delay)

    def read(self):
        with self.lock:
            return self.frame is not None, self.frame

    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join(timeout=1.0)
        if self.stream:
            self.stream.release()
            
    @staticmethod
    def test_connection(source):
        """Quickly test connection without starting a thread"""
        try:
            cap = None
            if isinstance(source, int) or (isinstance(source, str) and source.isdigit()):
                # Webcam Logic
                src = int(source)
                if os.name == 'nt':
                    cap = cv2.VideoCapture(src, cv2.CAP_DSHOW)
                    if not cap.isOpened():
                         cap = cv2.VideoCapture(src)
                else:
                    cap = cv2.VideoCapture(src)
            else:
                # RTSP Logic
                os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;tcp"
                cap = cv2.VideoCapture(source, cv2.CAP_FFMPEG)

            if cap and cap.isOpened():
                ret, frame = cap.read()
                cap.release()
                return ret
            return False
        except Exception as e:
            print(f"Connection test error: {e}")
            return False
