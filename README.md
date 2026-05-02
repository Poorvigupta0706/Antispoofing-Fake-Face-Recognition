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

## Output
<img width="1920" height="1080" alt="Screenshot (213)" src="https://github.com/user-attachments/assets/6201d108-b99c-4144-a4de-a86df5b3d3a5" />


