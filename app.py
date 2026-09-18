import cv2
import mediapipe as mp
import math
import pygame

# Initialize sound mixer
pygame.mixer.init()
gun_sound = pygame.mixer.Sound("gunshot.wav")

CAMERA_URL = "http://192.168.0.176:8080/video" # IP webcam url

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

# Custom visual styles matching the screenshots: Cyan lines + White landmark circles
landmark_style = mp_drawing.DrawingSpec(color=(255, 255, 255), thickness=-1, circle_radius=5)
connection_style = mp_drawing.DrawingSpec(color=(180, 230, 30), thickness=2)

cap = cv2.VideoCapture(CAMERA_URL)

bullets = []
flash_counter = 0
was_cocked = False

def dist_3d(p1, p2):
    return math.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2 + (p1.z - p2.z)**2)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("Waiting for camera frame...")
        break

    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    status_text = "Searching Hand..."
    status_color = (150, 150, 150)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            lm = hand_landmarks.landmark

            # 1. Draw full hand skeleton with joints
            mp_drawing.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS,
                landmark_drawing_spec=landmark_style,
                connection_drawing_spec=connection_style
            )

            # 2. Scale-Invariant Normalization using palm base length
            palm_scale = dist_3d(lm[0], lm[9])
            if palm_scale == 0:
                continue

            # Normalized distances
            d_mid   = dist_3d(lm[12], lm[0]) / palm_scale
            d_ring  = dist_3d(lm[16], lm[0]) / palm_scale
            d_pinky = dist_3d(lm[20], lm[0]) / palm_scale
            d_index = dist_3d(lm[8], lm[0]) / palm_scale
            d_index_knuckle = dist_3d(lm[5], lm[0]) / palm_scale

            # Thumb distance to index knuckle
            thumb_ratio = dist_3d(lm[4], lm[5]) / palm_scale

            # 3. Finger gun pose validation
            is_curled = (d_mid < 1.05) and (d_ring < 1.0) and (d_pinky < 0.95)
            is_index_out = d_index > (d_index_knuckle * 1.35)
            is_gun = is_curled and is_index_out

            tip_px = (int(lm[8].x * w), int(lm[8].y * h))

            if is_gun:
                # Highlight index tip with red target marker
                cv2.circle(frame, tip_px, 8, (0, 0, 255), -1)

                # Cock the thumb up
                if thumb_ratio > 0.65:
                    was_cocked = True
                    status_text = "READY / COCKED"
                    status_color = (0, 255, 255)

                # Pull trigger (snap thumb down)
                elif thumb_ratio < 0.45 and was_cocked:
                    was_cocked = False
                    flash_counter = 5
                    status_text = "BANG!"
                    status_color = (0, 0, 255)
                    gun_sound.play()

                    # Direction vector from Knuckle (5) to Tip (8)
                    base_px = (int(lm[5].x * w), int(lm[5].y * h))
                    vx = tip_px[0] - base_px[0]
                    vy = tip_px[1] - base_px[1]
                    mag = math.hypot(vx, vy) or 1
                    speed = 45

                    bullets.append({
                        'x': float(tip_px[0]),
                        'y': float(tip_px[1]),
                        'vx': (vx / mag) * speed,
                        'vy': (vy / mag) * speed,
                        'life': 30
                    })
                else:
                    status_text = "AIMING"
                    status_color = (0, 255, 0)
            else:
                status_text = "HAND DETECTED"
                status_color = (255, 255, 0)

    # Render Muzzle Flash
    if flash_counter > 0 and results.multi_hand_landmarks:
        lm = results.multi_hand_landmarks[0].landmark
        fx, fy = int(lm[8].x * w), int(lm[8].y * h)
        cv2.circle(frame, (fx, fy), 32, (0, 255, 255), -1)
        cv2.circle(frame, (fx, fy), 16, (255, 255, 255), -1)
        flash_counter -= 1

    # Render Bullets
    for b in bullets[:]:
        b['x'] += b['vx']
        b['y'] += b['vy']
        b['life'] -= 1

        start_pt = (int(b['x']), int(b['y']))
        end_pt = (int(b['x'] - b['vx'] * 0.7), int(b['y'] - b['vy'] * 0.7))
        cv2.line(frame, start_pt, end_pt, (0, 140, 255), 4)

        if b['life'] <= 0 or not (0 <= b['x'] <= w and 0 <= b['y'] <= h):
            bullets.remove(b)

    # Overlay HUD status text
    cv2.putText(frame, f"STATUS: {status_text}", (20, 40), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.9, status_color, 2, cv2.LINE_AA)

    cv2.imshow("Finger Gun Detector", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()