class FallDetector:
    def __init__(self, stand_threshold= 0.33, sit_threshold = 0.22 , fall_threshold = 0.10):
        
        """ 
        Umbrales:
        stand_threshold: Umbral para detectar si una persona está de pie.
        sit_threshold: Umbral para detectar si una persona está sentada.
        fall_threshold: Umbral para detectar una caída.
        """
        self.stand_threshold = stand_threshold
        self.sit_threshold = sit_threshold
        self.fall_threshold = fall_threshold
    
    def avg_y(self, p1, p2):
        return (p1.y + p2.y) / 2
    
    def torso_vertical(self, ls, rs, lh, rh):
        """
        Calcula la distancia vertical entre los hombros y las caderas.
        """
        avg_shoulder_y = self.avg_y(ls, rs)
        avg_hip_y = self.avg_y(lh, rh)
        return abs(avg_shoulder_y - avg_hip_y)
    
    def leg_fold_amount(self, lh, rh, lk, rk):
        avg_hip_y = self.avg_y(lh, rh)
        avg_knee_y = self.avg_y(lk, rk)
        return abs(avg_hip_y - avg_knee_y)

    def obtener_estado(self, ls, rs, lh, rh, lk, rk):
        """
        Determina el estado de la persona (de pie, sentada o caída) basado en las posiciones de los puntos clave.
        
        Parámetros:
        ls: Punto clave del hombro izquierdo.
        rs: Punto clave del hombro derecho.
        lh: Punto clave de la cadera izquierda.
        rh: Punto clave de la cadera derecha.
        
        Retorna:
        Un string que indica el estado: "de pie", "sentada" o "caída".
        """
        torso_height = self.torso_vertical(ls, rs, lh, rh)
        leg_fold = self.leg_fold_amount(lh, rh, lk, rk)

        # Persona de pie: torso alto y piernas estiradas
        if torso_height > self.stand_threshold and leg_fold > 0.25:
            return "de pie"

        # Sentado: torso bajo, piernas dobladas
        if torso_height < self.stand_threshold and leg_fold < 0.25:
            return "sentada"

        # Caído: torso muy bajo PERO piernas casi estiradas (no dobladas como sentado)
        if torso_height < self.sit_threshold and leg_fold > 0.20:
            return "caída"

        return "desconocido"