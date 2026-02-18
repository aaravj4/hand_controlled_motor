import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import numpy as np
import serial
import time
import os

# ===================== SERIAL =====================

SERIAL_PORT = '/dev/cu.usbmodem14101' #<-- CHANGE port
BAUD_RATE = 115200

esp = serial.Serial()
esp.port = SERIAL_PORT
esp.baudrate = BAUD_RATE
esp.timeout = 1
esp.open()

time.sleep(3)  # allow Arduino to reset

motor_state = None

# ===================== MEDIAPIPE =====================

model_path = os.path.join(os.path.dirname(__file__), "hand_landmarker.task")

base_options = python.BaseOptions(model_asset_path=model_path)

options = vision.HandLandmarkerOptions(
    base_options=base_options,
    num_hands=1,
    min_hand_detection_confidence=0.5,
    min_hand_presence_confidence=0.5,
    min_tracking_confidence=0.5
)

detector = vision.HandLandmarker.create_from_options(options)

cap = cv2.VideoCapture(0)

# ===================== HAND LOGIC =====================

def is_hand_open(landmarks):
    tips = [8, 12, 16, 20]
    open_fingers = 0

    for tip in tips:
        if landmarks[tip].y < landmarks[tip - 2].y:
            open_fingers += 1

    return open_fingers >= 3


def draw_hand_landmarks(img, landmarks):
    h, w, _ = img.shape

    for landmark in landmarks:
        x = int(landmark.x * w)
        y = int(landmark.y * h)
        cv2.circle(img, (x, y), 5, (0, 255, 0), -1)

    connections = [
        (0,1),(1,2),(2,3),(3,4),
        (0,5),(5,6),(6,7),(7,8),
        (0,9),(9,10),(10,11),(11,12),
        (0,13),(13,14),(14,15),(15,16),
        (0,17),(17,18),(18,19),(19,20),
        (5,9),(9,13),(13,17)
    ]

    for start_idx, end_idx in connections:
        start = landmarks[start_idx]
        end = landmarks[end_idx]
        start_point = (int(start.x * w), int(start.y * h))
        end_point = (int(end.x * w), int(end.y * h))
        cv2.line(img, start_point, end_point, (255, 255, 255), 2)

    return img

# ===================== MAIN FUNC =====================

try:
    while True:
        success, img = cap.read()
        if not success:
            continue

        rgb_frame = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)

        detection_result = detector.detect(mp_image)

        if detection_result.hand_landmarks:
            landmarks = detection_result.hand_landmarks[0]

            if is_hand_open(landmarks):
                cv2.putText(img, "MOTOR ON", (20,50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

                if motor_state != "ON":
                    if esp.is_open:
                        esp.write(b'ON\n')
                    motor_state = "ON"

            else:
                cv2.putText(img, "MOTOR OFF", (20,50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)

                if motor_state != "OFF":
                    if esp.is_open:
                        esp.write(b'OFF\n')
                    motor_state = "OFF"

            img = draw_hand_landmarks(img, landmarks)

        cv2.imshow("Hand Control", img)

        if cv2.waitKey(1) & 0xFF == 27:
            break

        time.sleep(0.02)

except KeyboardInterrupt:
    pass

finally:
    cap.release()
    cv2.destroyAllWindows()
    if esp.is_open:
        esp.close()
