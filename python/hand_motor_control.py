import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import serial
import time

# -------------------- ESP32 Serial --------------------
PORT = "COM3"       # Replace with your ESP32 COM port
BAUD_RATE = 115200
ser = serial.Serial(PORT, BAUD_RATE, dsrdtr=False, timeout=1)
time.sleep(2)

# -------------------- Hand Landmarker --------------------
base_options = python.BaseOptions(
    model_asset_path=r"C:\Users\jaina\OneDrive\Documents\PlatformIO\Projects\hand_controlled_motor\python\hand_landmarker.task"
)
options = vision.HandLandmarkerOptions(
    base_options=base_options,
    num_hands=1,
    min_hand_detection_confidence=0.5,
    min_hand_presence_confidence=0.5,
    min_tracking_confidence=0.5
)
detector = vision.HandLandmarker.create_from_options(options)

cap = cv2.VideoCapture(0)

def is_hand_open(landmarks):
    tips = [8, 12, 16, 20]
    open_fingers = 0
    for tip in tips:
        if landmarks[tip].y < landmarks[tip - 2].y:
            open_fingers += 1
    return open_fingers >= 3

def draw_hand_landmarks(img, landmarks):
    h, w, c = img.shape
    for i, landmark in enumerate(landmarks):
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
        cv2.line(img, (int(start.x*w), int(start.y*h)),
                 (int(end.x*w), int(end.y*h)), (255,255,255), 2)
    return img

prev_state = None

while True:
    success, img = cap.read()
    if not success:
        continue
    rgb_frame = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
    detection_result = detector.detect(mp_image)

    motor_state = 0
    if detection_result.hand_landmarks:
        landmarks = detection_result.hand_landmarks[0]
        motor_state = 1 if is_hand_open(landmarks) else 0
        img = draw_hand_landmarks(img, landmarks)
        cv2.putText(img,
                    "MOTOR ON" if motor_state else "MOTOR OFF",
                    (20,50), cv2.FONT_HERSHEY_SIMPLEX, 1,
                    (0,255,0) if motor_state else (0,0,255), 2)

    if motor_state != prev_state:
        ser.write(str(motor_state).encode())
        prev_state = motor_state

    cv2.imshow("Hand Motor Control", img)
    if cv2.waitKey(1) & 0xFF == 27:
        ser.write(b"0")
        break

cap.release()
cv2.destroyAllWindows()
ser.close()
