import time
from collections import deque

class FallDetector:
    def __init__(self):
        # Suavizado temporal
        self.knee_hip_hist = deque(maxlen=5)
        self.body_height_hist = deque(maxlen=5)

        # Estado persistente
        self.last_state = None
        self.state_count = 0
        
        self.fall_start_time = None
        self.fall_confirmed = False

    def smooth(self, value, hist):
        hist.append(value)
        return sum(hist) / len(hist)

    # ------------------------------------
    # CLASIFICADOR DE POSTURA (TOP-DOWN)
    # ------------------------------------
    def classify_posture(self, lm):

        ls = lm["left_shoulder"]
        rs = lm["right_shoulder"]
        lh = lm["left_hip"]
        rh = lm["right_hip"]
        lk = lm["left_knee"]
        rk = lm["right_knee"]

        # Promedios
        shoulder_y = (ls[1] + rs[1]) / 2
        hip_y = (lh[1] + rh[1]) / 2
        knee_y = (lk[1] + rk[1]) / 2

        # Métricas CLAVE para cámara alta
        knee_hip = abs(knee_y - hip_y)
        body_height = abs(shoulder_y - hip_y)

        # Suavizado
        knee_hip = self.smooth(knee_hip, self.knee_hip_hist)
        body_height = self.smooth(body_height, self.body_height_hist)

        # -----------------------------
        # CLASIFICACIÓN
        # -----------------------------
        if body_height < 0.09:
            state = "Caído"

        elif knee_hip < 0.08:
            state = "Sentado"

        else:
            state = "De pie"

        # -----------------------------
        # PERSISTENCIA (ANTI-PARPADEO)
        # -----------------------------
        if state == self.last_state:
            self.state_count += 1
        else:
            self.state_count = 1

        if self.state_count >= 3:
            self.last_state = state
        
        posture = self.last_state or state
        
        # Eventos
        
        event = None
        now = time.time()
        
        # Detección de caída prolongada
        if posture == "Caído":
            if self.fall_start_time is None:
                self.fall_start_time = now
            
            elif not self.fall_confirmed and now - self.fall_start_time >= 3:
                self.fall_confirmed = True
                event = "Caída confirmada"
        else:
            # Recuperacion
            if self.fall_confirmed:
                event = "Recuperación de caída"
            
            self.fall_start_time = None
            self.fall_confirmed = False
        return posture, event
            

