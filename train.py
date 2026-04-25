from ultralytics import YOLO
model=YOLO('yolov8n.pt')
model.train(data=r'C:\Users\dell\Desktop\Antispoofing\Dataset\SplitData\data.yaml',epochs=20 )