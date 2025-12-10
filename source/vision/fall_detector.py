import cv2
import mediapipe as mp
from fall_detector import FallDetector
from chatbot import on_event

mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

detector = FallDetector()
url = "rtsp://admin:123456@192.168.100.61:554/stream1"

cap = cv2.VideoCapture(url)

with mp_pose.Pose(
        model_complexity=1,
        min_detection_confidence=0.6,
        min_tracking_confidence=0.6) as pose:

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(img)

        posture = "Desconocido"

        if results.pose_landmarks:
            lm = results.pose_landmarks.landmark

            def p(i):
                return (lm[i].x, lm[i].y)

            coords = {
                "left_shoulder": p(mp_pose.PoseLandmark.LEFT_SHOULDER),
                "right_shoulder": p(mp_pose.PoseLandmark.RIGHT_SHOULDER),
                "left_hip": p(mp_pose.PoseLandmark.LEFT_HIP),
                "right_hip": p(mp_pose.PoseLandmark.RIGHT_HIP),
                "left_knee": p(mp_pose.PoseLandmark.LEFT_KNEE),
                "right_knee": p(mp_pose.PoseLandmark.RIGHT_KNEE),
            }

            posture, event = detector.classify_posture(coords)
            # Si hay un evento, comunica a chat bot
            if event:
                on_event(event, posture)
                
            mp_drawing.draw_landmarks(
                frame,
                results.pose_landmarks,
                mp_pose.POSE_CONNECTIONS
            )

        # Colores
        if posture == "De pie":
            color = (0, 255, 0)
        elif posture == "Sentado":
            color = (0, 255, 255)
        elif posture == "Caído":
            color = (0, 0, 255)
        else:
            color = (200, 200, 200)

        cv2.putText(frame, posture, (30, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.4, color, 3)

        cv2.imshow("Detector", frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break

cap.release()
cv2.destroyAllWindows()
