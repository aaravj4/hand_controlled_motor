# Hand Controlled Motor — Windows + ESP32 (OpenCV)

This branch contains the **Windows + ESP32 prototype** for the hand-controlled motor project.  
The motor is controlled using **hand gestures detected via OpenCV and MediaPipe** on Windows, which sends commands to the ESP32 over serial.

---

## Project Structure
hand_controlled_motor/
├── src/ # Main source files (C code for ESP32)
│ └── main.c # Main ESP32 program
├── python/ # Python scripts for hand detection, model, requirements.txt
│ └── hand_motor_control.py # Uses OpenCV + MediaPipe to send motor commands
├── lib/ # Additional libraries
├── platformio.ini # PlatformIO project configuration
└── README.md # Project documentation


---

## Features

- Hand detection via webcam using OpenCV + MediaPipe  
- Sends motor ON/OFF commands to ESP32 over serial in real-time  
- ESP32 controls motor via MOSFET using PWM  
- Works on Windows with Python 3.x  

---

## Requirements

- ESP32 development board  
- PlatformIO installed in VSCode  
- Python 3.x  
- Install Python dependencies using `requirements.txt`:

```bash
pip install -r requirements.txt
```

## Running program
- git clone <your-repo-url>
- cd hand_controlled_motor
- git checkout windows-esp32
- cd python
- python hand_motor_control.py
