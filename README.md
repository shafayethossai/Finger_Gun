# Real-Time Finger Gun Detector 🎯🔫

A real-time Computer Vision application that turns your hand into a virtual laser gun using your phone's camera or a standard webcam. It uses MediaPipe for hand joint tracking, OpenCV for visualization, and Pygame for dynamic sound synthesis.

---

## What is this?

This project tracks 21 hand landmarks in real time and detects a "finger-gun" gesture. When you cock your thumb up (ready state) and snap it down toward your hand (hammer release), the system registers a shot, spawning:
- Real-time animated laser projectiles following your aiming vector.
- Visual muzzle flash effects.
- Instant gunshot sound effects.
- An interactive HUD displaying the current state (`AIMING`, `READY / COCKED`, `BANG!`).

---

## Tech Stack & Architecture

- **OpenCV (`cv2`)**: Captures video frames over an IP camera stream, handles coordinate rendering, and displays the UI HUD.
- **MediaPipe (`Hands`)**: Extracts 3D spatial coordinates across 21 skeletal joints per hand.
- **NumPy & Math**: Powers dynamic palm-scale normalization (ensuring gesture accuracy regardless of distance from the lens) and vector calculations for trajectory direction.
- **Pygame Mixer**: Delivers zero-latency audio playback for gunshot effects.

### How it Works

Phone (IP Webcam Feed) ──► OpenCV VideoCapture ──► MediaPipe (Joint Tracking)
│
▼
Display Window ◄── OpenCV Canvas / Pygame Audio ◄── Vector Geometry & State Machine

1. **Palm Normalization:** Distances between joints are divided by the base palm distance (wrist `0` to middle MCP `9`). This ensures the gesture triggers reliably whether the hand is close to the lens or far away.
2. **Gesture Recognition:**
   - **Extended Index Finger:** The distance from Landmark `8` to Wrist `0` is significantly larger than Landmark `5` to Wrist `0`.
   - **Curled Fingers:** Middle (`12`), Ring (`16`), and Pinky (`20`) tips are curled in toward the palm.
3. **Hammer Pull Mechanism:**
   - When the thumb tip (`4`) raises away from knuckle (`5`) (`ratio > 0.65`), the gun enters `READY / COCKED`.
   - When the thumb rapidly drops (`ratio < 0.45`), the state transitions to `BANG!`, dispatching a projectile along the vector $\vec{v} = (\text{Tip}_8 - \text{Knuckle}_5)$ and playing audio.

---

## Getting Started

Follow these steps to run the project locally on your machine.

### Prerequisites

- Python 3.9 – 3.11
- A smartphone with an IP camera app (e.g., **IP Webcam** on Android) OR a built-in PC webcam.
- Linux/Ubuntu, macOS, or Windows.

---

### Installation & Setup

1. **Clone the Repository**
   ```bash
   git clone [https://github.com/your-username/finger-gun-detector.git](https://github.com/your-username/finger-gun-detector.git)
   cd finger-gun-detector

1. Create and Activate a Virtual Environment
   Linux / macOS:
   python3 -m venv venv
   source venv/bin/activate


   Windows:
   python -m venv venv
   venv\Scripts\activate

2. Install Dependencies
   pip install opencv-python "mediapipe<0.10.15" pygame numpy

3. Generate the Gunshot Sound File
Run this one-line command to generate the required gunshot.wav file using Python's standard library:

python -c '
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

Camera Configuration: 
Option A: Using Your Phone as an IP Webcam (Recommended)

1. Install IP Webcam (by Pavel Khlebovich) from Google Play.
2. Ensure your phone and PC are connected to the same Wi-Fi network.
3. Open the app, scroll to the bottom, and tap Start server.
4. Note the IPv4 address displayed on screen (e.g., http://192.168.0.176:8080).
5. Open app.py and set:
   CAMERA_URL = "http://<YOUR_PHONE_IP>:8080/video"

Option B: Using a Built-in or USB Webcam
If using a standard PC webcam, change line 27 in app.py to:

  cap = cv2.VideoCapture(0)


Running the App
Execute the main script:
python app.py


Aim: Point your index finger at targets on screen.
Cock: Lift your thumb upright until the status displays READY / COCKED.
Shoot: Snap your thumb downward toward your hand.
Quit: Press q while focused on the video window to exit.

   
