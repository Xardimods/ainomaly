import os
import json
import time
import requests
import threading
import cv2
import queue
import uuid
from datetime import datetime

class AlertManager:
    def __init__(self, settings_file="alerts_settings.json", history_file="alerts_history.json"):
        self.settings_file = settings_file
        self.history_file = history_file
        self.notification_queue = queue.Queue()
        self.settings = self._load_settings()
        self.history = self._load_history()
        
        # State tracking
        self.camera_cooldowns = {} # {camera_id: last_alert_timestamp}
        self.ongoing_falls = {} # {camera_id: {start_time: float, alerted: bool}}
        self.active_recordings = {} # {camera_id: {writer: cv2.VideoWriter, path: str, start_time: float}}
        
    def _load_settings(self):
        defaults = {
            "telegram_token": "",
            "telegram_chat_ids": [], # Changed from single ID to list
            "enabled": False,
            "min_duration": 2.0, 
            "cooldown": 60, 
            "attach_image": True,
            "save_snapshot": True,
            "notification_duration": 5
        }

        settings = defaults.copy()
        
        if os.path.exists(self.settings_file):
            try:
                with open(self.settings_file, 'r') as f:
                    loaded = json.load(f)
                    settings.update(loaded)
                    
                    # Migration: Single ID to List
                    if "telegram_chat_id" in loaded and loaded["telegram_chat_id"]:
                        if loaded["telegram_chat_id"] not in settings["telegram_chat_ids"]:
                            settings["telegram_chat_ids"].append(loaded["telegram_chat_id"])
            except:
                pass
        
        return settings

    # ... (skipping unchanged) ...

    def test_connection(self, token=None, chat_id=None):
        token = token or self.settings.get("telegram_token")
        
        # If specific ID not provided, try to use first configured ID
        if not chat_id:
            configured_ids = self.settings.get("telegram_chat_ids", [])
            if configured_ids:
                chat_id = configured_ids[0]

        if not token:
            return False, "Falta el Token del bot", None
            
        found_chat_id = None
        
        # If still no chat_id, try to fetch (auto-detect)
        if not chat_id:
            fetched_id = self._fetch_chat_id(token)
            if fetched_id:
                chat_id = fetched_id
                found_chat_id = fetched_id
            else:
                return False, "No se encontró ningún Chat ID configurado ni detectado.", None

        # Try sending message
        success, msg = self._send_telegram_msg(token, chat_id, "🔔 Conexión exitosa con AInomaly.")
        
        if success:
            if found_chat_id:
                return True, f"¡Conectado! Se detectó el Chat ID: {found_chat_id}", found_chat_id
            return True, "Conexión verificada correctamente", None
        else:
            return False, f"Error: {msg}", None

    # ... (skipping discover_users and fetch_chat_id) ...


    def _save_settings(self):
        with open(self.settings_file, 'w') as f:
            json.dump(self.settings, f, indent=4)

    def _load_history(self):
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r') as f:
                    history = json.load(f)
                    # Backfill IDs if missing
                    modified = False
                    for h in history:
                        if "id" not in h:
                            h["id"] = str(uuid.uuid4())
                            modified = True
                    
                    if modified:
                        # Save back immediately if we added IDs
                        with open(self.history_file, 'w') as out:
                            json.dump(history, out, indent=4)
                            
                    return history
            except:
                pass
        return []

    def _save_history(self):
        # Keep last 100 alerts
        if len(self.history) > 100:
            self.history = self.history[-100:]
            
        with open(self.history_file, 'w') as f:
            json.dump(self.history, f, indent=4)

    def get_settings(self):
        return self.settings

    def update_settings(self, new_settings):
        self.settings.update(new_settings)
        self._save_settings()
        return self.settings

    def get_history(self):
        # Sort by date desc
        return sorted(self.history, key=lambda x: x['date'], reverse=True)


    def discover_users(self, token=None):
        token = token or self.settings.get("telegram_token")
        if not token:
            return []
            
        users = {}
        try:
            url = f"https://api.telegram.org/bot{token}/getUpdates"
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data.get("ok"):
                    for result in data.get("result", []):
                        chat = None
                        if "message" in result:
                            chat = result["message"]["chat"]
                        elif "my_chat_member" in result:
                            chat = result["my_chat_member"]["chat"]
                        elif "edited_message" in result:
                            chat = result["edited_message"]["chat"]
                            
                        if chat:
                            chat_id = str(chat["id"])
                            name = chat.get("username") or chat.get("title") or f"{chat.get('first_name', '')} {chat.get('last_name', '')}".strip()
                            type_ = chat.get("type", "private")
                            
                            users[chat_id] = {
                                "id": chat_id,
                                "name": name or f"User {chat_id}",
                                "type": type_
                            }
        except Exception as e:
            print(f"Error discovering users: {e}")
            
        return list(users.values())

    def _fetch_chat_id(self, token):
        try:
            url = f"https://api.telegram.org/bot{token}/getUpdates"
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data.get("ok") and data.get("result"):
                    # Get most recent message
                    last_update = data["result"][-1]
                    if "message" in last_update:
                        return str(last_update["message"]["chat"]["id"])
                    if "my_chat_member" in last_update:
                         return str(last_update["my_chat_member"]["chat"]["id"])
        except Exception as e:
            print(f"Error fetching updates: {e}")
        return None

    def _send_telegram_msg(self, token, chat_id, text, image=None):
        try:
            url = f"https://api.telegram.org/bot{token}/sendMessage"
            data = {"chat_id": chat_id, "text": text, "parse_mode": "HTML"}
            
            if image is not None:
                url = f"https://api.telegram.org/bot{token}/sendPhoto"
                files = {'photo': image}
                data = {"chat_id": chat_id, "caption": text, "parse_mode": "HTML"}
                response = requests.post(url, data=data, files=files, timeout=10)
            else:
                response = requests.post(url, data=data, timeout=10)
                
            if response.status_code == 200:
                return True, "Enviado"
            else:
                return False, f"Error API: {response.text}"
        except Exception as e:
            return False, str(e)

    def process_event(self, camera_id, camera_name, event_type, confidence, frame=None):
        """
        Main entry point for vision system to report events.
        """
        if not self.settings.get("enabled"):
            return

        now = time.time()
        
        # Logic for Fall Detection (Duration check)
        if event_type == "Caída detectada":
            if camera_id not in self.ongoing_falls:
                self.ongoing_falls[camera_id] = {"start_time": now, "alerted": False}
                return # Wait for duration
            else:
                # Check duration
                elapsed = now - self.ongoing_falls[camera_id]["start_time"]
                if elapsed < self.settings.get("min_duration", 0):
                    return # Not long enough yet
                
                if self.ongoing_falls[camera_id]["alerted"]:
                    return # Already alerted for this specific fall instance
        
        elif event_type == "Recuperación" or event_type == "Normal":
            if camera_id in self.ongoing_falls:
                # Stop recording if active and send result
                self.stop_recording(camera_id, camera_name)
                del self.ongoing_falls[camera_id]
            return

        # Cooldown Check
        last_alert = self.camera_cooldowns.get(camera_id, 0)
        cooldown = self.settings.get("cooldown", 60)
        
        if now - last_alert < cooldown:
            print(f"[AlertManager] Ignorando alerta por cooldown para {camera_name}")
            return

        # Trigger Alert
        self._trigger_alert(camera_id, camera_name, event_type, confidence, frame)
        
        # Start recording immediately
        self.start_recording(camera_id, frame)
        
        # Update state
        self.camera_cooldowns[camera_id] = now
        if camera_id in self.ongoing_falls:
            self.ongoing_falls[camera_id]["alerted"] = True

    def _trigger_alert(self, camera_id, camera_name, event_type, confidence, frame):
        # Prepare content
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        title = "⚠️ <b>ALERTA DE SEGURIDAD</b>"
        
        msg = (
            f"{title}\n\n"
            f"<b>Cámara:</b> {camera_name}\n"
            f"<b>Evento:</b> {event_type}\n"
            f"<b>Confianza:</b> {confidence:.0%}\n"
            f"<b>Hora:</b> {timestamp}\n"
        )

        image_bytes = None
        snapshot_path = None
        
        if self.settings.get("attach_image") and frame is not None:
            try:
                # Encode for Telegram
                success, buffer = cv2.imencode(".jpg", frame)
                if success:
                    image_bytes = buffer.tobytes()
                    
                    # Save snapshot to disk (optional)
                    if self.settings.get("save_snapshot"):
                         snapshots_dir = "snapshots"
                         os.makedirs(snapshots_dir, exist_ok=True)
                         filename = f"alert_{camera_id}_{int(time.time())}.jpg"
                         snapshot_path = os.path.join(snapshots_dir, filename)
                         with open(snapshot_path, "wb") as f:
                             f.write(image_bytes)
            except Exception as e:
                print(f"Error preparing snapshot: {e}")

        # Send in background thread to not block vision loop
        threading.Thread(target=self._dispatch_alert, 
                         args=(msg, image_bytes, camera_id, camera_name, event_type, snapshot_path)
        ).start()

    def _dispatch_alert(self, msg, image_bytes, camera_id, camera_name, event_type, snapshot_path):
        token = self.settings.get("telegram_token")
        chat_ids = self.settings.get("telegram_chat_ids", [])
        
        if not token or not chat_ids:
            print("[AlertManager] No token/chat_ids configured.")
            return

        # Send to all recipients
        any_success = False
        details_log = []
        
        for chat_id in chat_ids:
            success, response_text = self._send_telegram_msg(token, chat_id, msg, image_bytes)
            if success:
                any_success = True
            details_log.append(f"{chat_id}: {'OK' if success else 'ERR'}")

        # Log to history
        entry = {
            "id": str(uuid.uuid4()),
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "camera": camera_name,
            "event": event_type,
            "status": "Enviado" if any_success else "Fallido",
            "details": ", ".join(details_log),
            "snapshot": snapshot_path
        }
        self.history.append(entry)
        self._save_history()
        print(f"[AlertManager] Alerta procesada. Enviada a {len(chat_ids)} destinatarios.")

    def delete_alert(self, alert_id):
        initial_len = len(self.history)
        self.history = [a for a in self.history if a.get("id") != alert_id]
        if len(self.history) < initial_len:
            self._save_history()
            return True
        return False

    def start_recording(self, camera_id, frame):
        if not self.settings.get("enabled", False):
           return

        # If already recording, ignore
        if camera_id in self.active_recordings:
            return

        try:
            recordings_dir = "recordings"
            if not os.path.exists(recordings_dir):
                os.makedirs(recordings_dir)
            
            timestamp = int(time.time())
            filename = f"event_{camera_id}_{timestamp}.mp4"
            filepath = os.path.join(recordings_dir, filename)
            
            height, width = frame.shape[:2]
            # 'avc1' is H.264, best for HTML5/Electron playback. 
            # If this fails, try 'vp80' or 'mp4v' (but mp4v often fails in browser)
            try:
                fourcc = cv2.VideoWriter_fourcc(*'avc1') 
                writer = cv2.VideoWriter(filepath, fourcc, 20.0, (width, height))
                if not writer.isOpened():
                    # Fallback if avc1 is not supported on this OS
                    print("[AlertManager] H.264 codec not found, falling back to mp4v")
                    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
                    writer = cv2.VideoWriter(filepath, fourcc, 20.0, (width, height))
            except:
                 fourcc = cv2.VideoWriter_fourcc(*'mp4v')
                 writer = cv2.VideoWriter(filepath, fourcc, 20.0, (width, height))
            
            self.active_recordings[camera_id] = {
                "writer": writer,
                "path": filepath,
                "start_time": time.time(),
                "frames": 0
            }
            print(f"[AlertManager] Recording started for {camera_id}: {filepath}")
        except Exception as e:
            print(f"[AlertManager] Failed to start recording: {e}")

    def write_frame(self, camera_id, frame):
        if camera_id in self.active_recordings:
            try:
                rec = self.active_recordings[camera_id]
                rec["writer"].write(frame)
                rec["frames"] += 1
            except Exception as e:
                print(f"Error writing frame: {e}")

    def stop_recording(self, camera_id, camera_name="Cámara"):
        if camera_id not in self.active_recordings:
            return

        rec = self.active_recordings.pop(camera_id)
        try:
            rec["writer"].release()
            duration = time.time() - rec["start_time"]
            print(f"[AlertManager] Recording stopped for {camera_id}. Duration: {duration:.1f}s")
            
            # Send via Telegram
            self._send_video_alert(rec["path"], camera_name, duration)
        except Exception as e:
            print(f"[AlertManager] Error stopping recording: {e}")

    def _send_video_alert(self, filepath, camera_name, duration):
        threading.Thread(target=self._dispatch_video, args=(filepath, camera_name, duration)).start()

    def _dispatch_video(self, filepath, camera_name, duration):
        token = self.settings.get("telegram_token")
        chat_ids = self.settings.get("telegram_chat_ids", [])
        
        if not token or not chat_ids:
            return
            
        msg = f"🎥 <b>Evento Registrado</b>\n<b>Cámara:</b> {camera_name}\n<b>Duración:</b> {duration:.1f}s"
        
        try:
            with open(filepath, 'rb') as video:
                files = {'video': video}
                for chat_id in chat_ids:
                    video.seek(0) 
                    url = f"https://api.telegram.org/bot{token}/sendVideo"
                    data = {"chat_id": chat_id, "caption": msg, "parse_mode": "HTML"}
                    requests.post(url, data=data, files={'video': video}, timeout=60)
            print(f"[AlertManager] Video enviado a Telegram.")
        except Exception as e:
            print(f"[AlertManager] Error enviando video: {e}")
