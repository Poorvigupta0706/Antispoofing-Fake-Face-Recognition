import math
import time
import cv2
import cvzone
from ultralytics import YOLO

confidence = 0.6

# Camera
cap = cv2.VideoCapture(0)  # try 0 first
cap.set(3, 640)
cap.set(4, 480)

# Load model
model = YOLO("../models/l_version_1_300.pt")

classNames = ["fake", "real"]

prev_frame_time = 0

while True:
    success, img = cap.read()

    if not success or img is None:
        print("❌ Camera error")
        continue

    new_frame_time = time.time()

    results = model(img, stream=True, verbose=False)

    for r in results:
        boxes = r.boxes

        for box in boxes:
            # Bounding box
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            w, h = x2 - x1, y2 - y1

            # Confidence
            conf = float(box.conf[0])

            # Class
            cls = int(box.cls[0])

            if conf > confidence:

                if classNames[cls] == 'real':
                    color = (0, 255, 0)
                else:
                    color = (0, 0, 255)

                # Draw box
                cvzone.cornerRect(img, (x1, y1, w, h),
                                  colorC=color, colorR=color)

                cvzone.putTextRect(
                    img,
                    f'{classNames[cls].upper()} {int(conf*100)}%',
                    (max(0, x1), max(35, y1)),
                    scale=2,
                    thickness=3,
                    colorR=color,
                    colorB=color
                )

    # FPS
    if prev_frame_time != 0:
        fps = 1 / (new_frame_time - prev_frame_time)
        cv2.putText(img, f'FPS: {int(fps)}', (20, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    prev_frame_time = new_frame_time

    cv2.imshow("Image", img)

    if cv2.waitKey(1) & 0xFF == 27:  # ESC to exit
        break

cap.release()
cv2.destroyAllWindows()