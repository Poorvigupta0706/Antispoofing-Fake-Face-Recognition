from cvzone.FaceDetectionModule import FaceDetector
import cv2
from time import time
import os

cap = cv2.VideoCapture(1)  # IMPORTANT: use 0
detector = FaceDetector()

classID = 1  # 0=fake, 1=real
baseFolderPath = 'Dataset/DataCollect'

confidence = 0.8
save = True
blurThreshold = 35

# Create folders
realPath = os.path.join(baseFolderPath, "real")
fakePath = os.path.join(baseFolderPath, "fake")

os.makedirs(realPath, exist_ok=True)
os.makedirs(fakePath, exist_ok=True)

while True:
    success, img = cap.read()

    if not success or img is None:
        print("❌ Camera error")
        continue

    img, bboxes = detector.findFaces(img)

    listInfo = []
    listBlur = []

    if bboxes:
        ih, iw, _ = img.shape

        for bbox in bboxes:
            x, y, w, h = bbox["bbox"]
            score = bbox["score"][0]

            if score > confidence:

                face = img[y:y+h, x:x+w]

                if face.size != 0:

                    blurValue = int(cv2.Laplacian(face, cv2.CV_64F).var())

                    if blurValue > blurThreshold:
                        listBlur.append(True)
                        color = (0, 255, 0)
                    else:
                        listBlur.append(False)
                        color = (0, 0, 255)

                    # NORMALIZATION
                    xc = x + w / 2
                    yc = y + h / 2

                    xcn = round(xc / iw, 6)
                    ycn = round(yc / ih, 6)
                    wn = round(w / iw, 6)
                    hn = round(h / ih, 6)

                    listInfo.append(f"{classID} {xcn} {ycn} {wn} {hn}\n")

                    # Draw
                    cv2.rectangle(img, (x, y, w, h), color, 2)
                    cv2.putText(img, f"{blurValue}", (x, y - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

        # -------- SAVE --------
        if save and all(listBlur) and listBlur != []:

            timeNow = str(time()).replace('.', '')

            # Select folder
            if classID == 1:
                savePath = realPath
            else:
                savePath = fakePath

            # Save image
            imgPath = f"{savePath}/{timeNow}.jpg"
            cv2.imwrite(imgPath, img)

            # Save label
            with open(f"{savePath}/{timeNow}.txt", 'w') as f:
                for info in listInfo:
                    f.write(info)

            print(f"✅ Saved in {savePath}: {timeNow}")

    cv2.imshow("Image", img)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()