# Antispoofing Fake Face Recognition 👁️

A lightweight **face recognition system with anti-spoofing** using **eye blink detection** for liveness verification.

---

## 🚀 Features

* Face detection & recognition
* Eye blink-based liveness detection
* Prevents spoofing (photo/video attacks)
* Real-time webcam support

---

## ⚙️ Installation

```bash
git clone https://github.com/poorvigupta0706/Antispoofing-Fake-Face-Recognition.git
cd Antispoofing-Fake-Face-Recognition
pip install -r requirements.txt
```

---

## ▶️ Usage

```bash
python detect.py
```

---

## 👁️ How It Works

* Detect face using OpenCV/dlib
* Calculate Eye Aspect Ratio (EAR)
* Blink detected → Real user ✅
* No blink → Spoof attempt ❌

---


