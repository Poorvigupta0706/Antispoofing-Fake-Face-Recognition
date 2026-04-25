# from time import time
# import cv2
# import os
# classID = 0
# outputFolderPath = 'Dataset/DataCollect'
# confidence = 1.1  
# save = True
# blurThreshold = 35

# offsetPercentageW = 10
# offsetPercentageH = 20
# camWidth, camHeight = 640, 480
# floatingPoint = 6

# os.makedirs(outputFolderPath, exist_ok=True)

# faceCascade = cv2.CascadeClassifier(
#     cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
# )

# cap = cv2.VideoCapture(0)
# cap.set(3, camWidth)
# cap.set(4, camHeight)

# if not cap.isOpened():
#     print("❌ Camera not working")
#     exit()

# while True:
#     success, img = cap.read()
#     if not success:
#         print("❌ Failed to read frame")
#         continue

#     imgOut = img.copy()
#     gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

#     faces = faceCascade.detectMultiScale(gray, 1.2, 5)

#     listBlur = []
#     listInfo = []

#     for (x, y, w, h) in faces:

#         # Offsets
#         offsetW = int((offsetPercentageW / 100) * w)
#         offsetH = int((offsetPercentageH / 100) * h)

#         x = max(0, x - offsetW)
#         y = max(0, y - offsetH * 3)
#         w = max(0, w + offsetW * 2)
#         h = max(0, h + int(offsetH * 3.5))

        
#         imgFace = img[y:y + h, x:x + w]
#         if imgFace.size == 0:
#             continue

#         cv2.imshow("Face", imgFace)

#         # Blur detection
#         blurValue = int(cv2.Laplacian(imgFace, cv2.CV_64F).var())
#         listBlur.append(blurValue > blurThreshold)

#         # Normalize values (YOLO format)
#         ih, iw, _ = img.shape
#         xc, yc = x + w / 2, y + h / 2

#         xcn = min(1, round(xc / iw, floatingPoint))
#         ycn = min(1, round(yc / ih, floatingPoint))
#         wn = min(1, round(w / iw, floatingPoint))
#         hn = min(1, round(h / ih, floatingPoint))

#         listInfo.append(f"{classID} {xcn} {ycn} {wn} {hn}\n")

#         # Draw rectangle
#         cv2.rectangle(imgOut, (x, y), (x + w, y + h), (255, 0, 0), 2)

#         cv2.putText(
#             imgOut,
#             f'Blur: {blurValue}',
#             (x, y - 10),
#             cv2.FONT_HERSHEY_SIMPLEX,
#             0.7,
#             (0, 255, 0),
#             2
#         )

#     # Save data
#     if save and listBlur and all(listBlur):
#         timeNow = str(time()).replace('.', '')
#         imgPath = f"{outputFolderPath}/{timeNow}.jpg"
#         txtPath = f"{outputFolderPath}/{timeNow}.txt"

#         cv2.imwrite(imgPath, img)

#         with open(txtPath, 'a') as f:
#             f.writelines(listInfo)

#     cv2.imshow("Image", imgOut)

#     if cv2.waitKey(1) & 0xFF == 27:  # ESC key
#         break

# cap.release()
# cv2.destroyAllWindows()