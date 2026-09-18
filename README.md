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
