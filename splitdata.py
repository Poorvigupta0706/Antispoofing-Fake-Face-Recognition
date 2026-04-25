import os
import random
import shutil
from itertools import islice

inputFolderPath = "Dataset/DataCollect"
outputFolderPath = "Dataset/SplitData"

splitRatio = {"train": 0.7, "val": 0.2, "test": 0.1}
classes = ["fake", "real"]

# Clean output folder
if os.path.exists(outputFolderPath):
    shutil.rmtree(outputFolderPath)

# Create folders
for split in ["train", "val", "test"]:
    os.makedirs(f"{outputFolderPath}/{split}/images", exist_ok=True)
    os.makedirs(f"{outputFolderPath}/{split}/labels", exist_ok=True)

# -------- GET FILES FROM real + fake --------
data = []

for classID, className in enumerate(classes):
    classPath = os.path.join(inputFolderPath, className)

    if not os.path.exists(classPath):
        print(f"❌ Missing folder: {classPath}")
        continue

    for file in os.listdir(classPath):
        if file.endswith(".jpg"):
            name = file.split('.')[0]
            data.append((name, className))

# Shuffle
random.shuffle(data)

# Split
lenData = len(data)
lenTrain = int(lenData * splitRatio['train'])
lenVal = int(lenData * splitRatio['val'])
lenTest = lenData - (lenTrain + lenVal)

trainData = data[:lenTrain]
valData = data[lenTrain:lenTrain+lenVal]
testData = data[lenTrain+lenVal:]

print(f"Total Images: {lenData}")
print(f"Train: {len(trainData)}, Val: {len(valData)}, Test: {len(testData)}")

# -------- COPY FILES --------
def copyFiles(dataset, splitName):
    for name, className in dataset:
        imgPath = f"{inputFolderPath}/{className}/{name}.jpg"
        labelPath = f"{inputFolderPath}/{className}/{name}.txt"

        if os.path.exists(imgPath) and os.path.exists(labelPath):
            shutil.copy(imgPath, f"{outputFolderPath}/{splitName}/images/{name}.jpg")
            shutil.copy(labelPath, f"{outputFolderPath}/{splitName}/labels/{name}.txt")
        else:
            print(f"⚠️ Missing: {name}")

copyFiles(trainData, "train")
copyFiles(valData, "val")
copyFiles(testData, "test")

print("✅ Split Done")

# -------- YAML --------
dataYaml = f"""path: C:/Users/dell/Desktop/Antispoofing/Dataset/SplitData

train: train/images
val: val/images
test: test/images

nc: {len(classes)}
names: {classes}
"""

with open(f"{outputFolderPath}/data.yaml", 'w') as f:
    f.write(dataYaml)

print("✅ data.yaml Created")