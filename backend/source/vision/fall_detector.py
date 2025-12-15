import time
from collections import deque


class FallDetector:
    def __init__(self):
        # Suavizado temporal
        self.knee_hip_hist = deque(maxlen=9)
        self.body_height_hist = deque(maxlen=9)
        self.shoulder_ankle_hist = deque(maxlen=9)

        # Estado visual estable
        self.last_state = None
        self.pending_state = None
        self.pending_since = None
        self.state_delay = 1.0  # segundos para cambiar estado

        # Caída (2 etapas)
        self.fall_state = None          # None | "Posible" | "Confirmada"
        self.fall_start_time = None
        self.confirm_time = 5.0         # segundos en el suelo

        # Debug
        self.debug = False

    def smooth(self, value, hist):
        hist.append(value)
        return sum(hist) / len(hist)

    
    # CLASIFICADOR DE POSTURA (TOP-DOWN)
    
    def classify_posture(self, lm):

        # Landmarks
        ls = lm["left_shoulder"]
        rs = lm["right_shoulder"]
        lh = lm["left_hip"]
        rh = lm["right_hip"]
        lk = lm["left_knee"]
        rk = lm["right_knee"]
        la = lm["left_ankle"]
        ra = lm["right_ankle"]

        # Promedios
        shoulder_y = (ls[1] + rs[1]) / 2
        hip_y = (lh[1] + rh[1]) / 2
        knee_y = max(lk[1], rk[1])
        ankle_y = max(la[1], ra[1])

        # Métricas TOP-DOWN
        knee_hip = abs(knee_y - hip_y)
        body_height = abs(shoulder_y - hip_y)
        shoulder_ankle = abs(shoulder_y - ankle_y)

        # Suavizado
        knee_hip = self.smooth(knee_hip, self.knee_hip_hist)
        body_height = self.smooth(body_height, self.body_height_hist)
        shoulder_ankle = self.smooth(shoulder_ankle, self.shoulder_ankle_hist)

        
        # CLASIFICACIÓN BASE (SIN TIEMPO)
        if shoulder_ankle < 0.15:
            detected_state = "Agachado"

        elif body_height < 0.09:
            detected_state = "Caido"

        elif knee_hip < 0.075:
            detected_state = "Sentado"

        else:
            detected_state = "De pie"

        
        # RETARDO DE CAMBIO DE ESTADO (ANTI-SALTOS)
        
        now = time.time()

        if detected_state != self.last_state:
            if self.pending_state != detected_state:
                self.pending_state = detected_state
                self.pending_since = now

            elif now - self.pending_since >= self.state_delay:
                self.last_state = detected_state
                self.pending_state = None
                self.pending_since = None
        else:
            self.pending_state = None
            self.pending_since = None

        posture = self.last_state or detected_state

        # CAÍDA EN DOS ETAPAS
        event = None

        if posture == "Caido":
            if self.fall_start_time is None:
                # Posible caída
                self.fall_start_time = now
                self.fall_state = "Posible"
                event = "Posible caida"

            elif self.fall_state == "Posible" and now - self.fall_start_time >= self.confirm_time:
                # Confirmación
                self.fall_state = "Confirmada"
                event = "Caida confirmada"

        else:
            if self.fall_state == "Confirmada":
                event = "Recuperación de caida"

            self.fall_state = None
            self.fall_start_time = None

        # DEBUG
        if self.debug:
            print(
                f"{posture:10s} | "
                f"SA={shoulder_ankle:.4f} | "
                f"BH={body_height:.4f} | "
                f"KH={knee_hip:.4f}"
            )

        return posture, event
