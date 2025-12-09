#Libreiras
import cv2 
import mediapipe as mp 
from fall_detector import FallDetector

#Inicializando mediapipe Pose
mp_drawing = mp.solutions.drawing_utils # Utilidad para dibujar puntos y conexiones
mp_pose = mp.solutions.pose # Solución de pose de mediapipe

detector = FallDetector()

# Abrir la camara
cap = cv2.VideoCapture(0) 

# Crear modelo de deteccion de pose
with mp_pose.Pose(
    static_image_mode=False, # Procesamiento en tiempo real (False = modelo trabaja mas rapido)
    model_complexity= 1, # Precision media para mejor rendimiento
    enable_segmentation=False, # No se necesita segmentacion
    min_detection_confidence=0.5, # Confianza minima para deteccion
    min_tracking_confidence=0.5 # Confianza minima para seguimiento
) as pose:
    
    while True:
        success, frame = cap.read() # Leer un frame de la camara
        frame = cv2.flip(frame, 1) # Voltear la imagen horizontalmente
        if not success:
            print("No se pudo acceder  la camara")
            break
        
        # Convertir la imagen de BGR(OpenCV) a RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Procesar la imagen con mediapipe Pose
        results = pose.process(rgb_frame)
        
        # Dibujar punto y conexiones si se detecta una pose
        if results.pose_landmarks:
            landmarks = results.pose_landmarks.landmark
            
            #Obtener coordenadas de los hombros
            left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER]
            right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER]
            
            #Obtener coordenadas de las caderas
            left_hip = landmarks[mp_pose.PoseLandmark.LEFT_HIP]
            right_hip = landmarks[mp_pose.PoseLandmark.RIGHT_HIP]
            
            # Obtener coordenadas de las rodillas
            left_knee = landmarks[mp_pose.PoseLandmark.LEFT_KNEE]
            right_knee = landmarks[mp_pose.PoseLandmark.RIGHT_KNEE]
            
            # Obtener coordenadas de los tobillos
            left_ankle  = landmarks[mp_pose.PoseLandmark.LEFT_ANKLE]
            right_ankle = landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE]

            
            # Obtener Estados
            estado = detector.obtener_estado(
                left_shoulder, right_shoulder,
                left_hip, right_hip,
                left_knee, right_knee,
              
            )
            
            cv2.putText(frame, f"Estado: {estado}", (10, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

            print("Estado:", estado)
            
            mp_drawing.draw_landmarks(
                frame, # Imagen donde se dibujara
                results.pose_landmarks, #Puntos detectados
                mp_pose.POSE_CONNECTIONS, # Conexiones entre puntos
                mp_drawing.DrawingSpec(color=(0,255,0), thickness=2, circle_radius=3),
                mp_drawing.DrawingSpec(color=(255,0,0), thickness=2)
            )
        # Mostrar la ventana
        cv2.imshow("Deteccion de Pose", frame)
        
        # Salir si se presiona la tecla 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
cap.release()
cv2.destroyAllWindows()