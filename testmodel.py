from ultralytics import YOLO
import cv2
import mediapipe as mp
import numpy as np

# Load YOLO model
model = YOLO("runs/detect/train3/weights/best.pt")

# Mediapipe setup
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(refine_landmarks=True)

cap = cv2.VideoCapture(1)

# Eye landmarks
LEFT_EYE = [33, 160, 158, 133, 153, 144]
RIGHT_EYE = [362, 385, 387, 263, 373, 380]

blink_counter = 0
blink_detected = False

def eye_aspect_ratio(landmarks, eye):
    p1 = landmarks[eye[0]]
    p2 = landmarks[eye[1]]
    p3 = landmarks[eye[2]]
    p4 = landmarks[eye[3]]
    p5 = landmarks[eye[4]]
    p6 = landmarks[eye[5]]

    v1 = np.linalg.norm(np.array([p2.x, p2.y]) - np.array([p6.x, p6.y]))
    v2 = np.linalg.norm(np.array([p3.x, p3.y]) - np.array([p5.x, p5.y]))
    h = np.linalg.norm(np.array([p1.x, p1.y]) - np.array([p4.x, p4.y]))

    return (v1 + v2) / (2.0 * h)


while True:
    success, img = cap.read()
    if not success:
        break

    h, w, _ = img.shape

    # YOLO detection
    results = model(img)

    # Mediapipe
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    mesh_results = face_mesh.process(rgb)

    # -------- BLINK DETECTION --------
    if mesh_results.multi_face_landmarks:
        for face_landmarks in mesh_results.multi_face_landmarks:

            leftEAR = eye_aspect_ratio(face_landmarks.landmark, LEFT_EYE)
            rightEAR = eye_aspect_ratio(face_landmarks.landmark, RIGHT_EYE)

            ear = (leftEAR + rightEAR) / 2.0

            if ear < 0.2:
                blink_counter += 1
            else:
                if blink_counter > 2:
                    blink_detected = True
                blink_counter = 0

    # -------- YOLO RESULT DRAW --------
    annotated = results[0].plot()

    # -------- FINAL DECISION --------
    if not blink_detected:
        cv2.putText(annotated, "FAKE (NO BLINK)",
                    (20, 50), cv2.FONT_HERSHEY_SIMPLEX,
                    1, (0, 0, 255), 3)

    else:
        cv2.putText(annotated, "REAL (BLINK DETECTED)",
                    (20, 50), cv2.FONT_HERSHEY_SIMPLEX,
                    1, (0, 255, 0), 3)

    cv2.imshow("Anti-Spoofing Advanced", annotated)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()