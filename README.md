# Real-Time Finger Gun Detector 🎯🔫

A real-time Computer Vision application that turns your hand into an interactive virtual laser gun using your smartphone's camera feed or a standard PC webcam. Built using MediaPipe for skeletal joint tracking, OpenCV for rendering and HUD display, and Pygame for dynamic sound synthesis.

---

## Overview

This project tracks 21 distinct hand landmarks in real time to recognize a finger-gun gesture. When you cock your thumb upright (ready state) and snap it down toward your palm (hammer release), the system registers a shot, generating:

- **Animated Laser Projectiles:** Dynamic bullets traveling along your exact aiming vector.
- **Muzzle Flash:** Visual expansion rings rendered at the fingertip upon firing.
- **Synthesized Audio:** Zero-latency gunshot sound effects triggered on state change.
- **Interactive HUD:** Live status indicators (`AIMING`, `READY / COCKED`, `BANG!`) reflecting hand posture.

---

## Tech Stack & Architecture

- **OpenCV (`cv2`)**: Captures video frames over an IP/RTSP stream, renders graphics, overlays HUD status, and handles window events.
- **MediaPipe (`Hands`)**: Performs real-time inference to extract normalized 3D coordinates for 21 skeletal hand landmarks.
- **NumPy & Math**: Implements scale-invariant joint normalization and calculates 2D/3D trajectory vectors.
- **Pygame Mixer**: Provides low-latency audio playback for gunshot sound effects.

### Architecture Pipeline

```text
Phone (IP Webcam Feed) ──► OpenCV VideoCapture ──► MediaPipe (Joint Inference)
                                                              │
                                                              ▼
Display Window (OpenCV) ◄── Visual Effects & Audio ◄── Geometric State Machine
```

1. Palm Normalization: All joint distances are divided by the base palm length (Wrist 0 to Middle MCP 9). This makes gesture detection scale-invariant regardless of your distance from the lens.

2. Gun Gesture Recognition:

   1. Index Finger Extended: Distance from Index Tip (8) to Wrist (0) is significantly greater than Index Knuckle (5) to Wrist (0).

   2. Curled Fingers: Tips of Middle (12), Ring (16), and Pinky (20) are curled inward toward the palm.

3. Trigger State Machine:

   1. Cocked State: When the thumb tip (4) raises away from knuckle (5) (ratio > 0.65), the gun enters READY / COCKED.

   2. Fire State: When the thumb rapidly snaps down (ratio < 0.45), the state transitions to BANG!, dispatching a projectile along the vector from landmark 5 to 8 and triggering audio.

## Getting Started
### Prerequisites
1. Python 3.9 – 3.11

2. A smartphone with an IP camera app (e.g., IP Webcam on Android) OR a built-in PC webcam

3. Linux/Ubuntu, macOS, or Windows

### Installation & Setup
1. Clone the Repository
```
git clone https://github.com/shafayethossai/Finger_Gun.git
cd Finger_Gun
```

2. Create and Activate a Virtual Environment

   1. Linux / macOS:
      ```
      python3 -m venv venv
      source venv/bin/activate
      ```

   2. Windows:
      ```
      python -m venv venv
      venv\Scripts\activate
      ```

3. Install Dependencies
```
pip install opencv-python "mediapipe<0.10.15" pygame numpy
```

5. Generate the Gunshot Sound File
Run this one-line command in your terminal to generate the required gunshot.wav audio file using Python's standard library:
```
python3 -c '
import wave, struct, random
rate, dur = 44100, 0.35
total = int(rate * dur)
with wave.open("gunshot.wav", "wb") as f:
    f.setnchannels(1); f.setsampwidth(2); f.setframerate(rate)
    for i in range(total):
        val = int(random.uniform(-1, 1) * ((1.0 - i / total) ** 3) * 32767)
        f.writeframesraw(struct.pack("<h", val))
print("Generated gunshot.wav successfully!")
'
```

### Camera Configuration
#### Option A: Using Your Smartphone as an IP Camera (Recommended)
1. Install IP Webcam (by Pavel Khlebovich) from the Google Play Store.

2. Connect your phone and computer to the same Wi-Fi network.

3. Open the app, scroll to the bottom, and tap Start server.

4. Note the IPv4 address shown on your screen (e.g., [http://192.168.0.176:8080](http://192.168.0.176:8080)).

5. Open app.py and set your URL:
   ```
   CAMERA_URL = "http://<YOUR_PHONE_IP>:8080/video"
   ```

#### Option B: Using a Built-in or USB Webcam
If using a standard PC webcam instead, change line 27 in app.py to:
```
cap = cv2.VideoCapture(0)
```

Running the Application
Execute the main script from your activated virtual environment:

python3 app.py

#### Controls
1. Aim: Point your extended index finger at the screen

2. Cock Gun: Raise your thumb upright until status displays READY / COCKED

3. Shoot: Snap your thumb downward toward your hand

4. Quit: Press q on your keyboard while focused on the video window
