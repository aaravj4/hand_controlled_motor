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

## Setup
1. After installing PlatformIO in VSCode:
2. New Project
3. Board: Espressif ESP32 Dev module
4. Framework: Espidf
5. Open platformio.ini(setup file), replicate platform.io in repository
6. pull src folder
7. Python folder may need to be created, pull 3 files:
8. hand_motor_control.py, requirements.txt, hand_landmarker.task
9. everything else should be the default settings for the PlatformIO project
10. Plug in ESP32
11. Click checkmark(build and upload) to flash code to ESP32
    
**Note**: Strongly recommend to not pull the entire repo into your local project path. Just clone the repo and get specific files and folders.


## Running program
- git clone <[https://github.com/aaravj4/hand_controlled_motor(https://github.com/aaravj4/hand_controlled_motor)>
- cd hand_controlled_motor
- git checkout windows-esp32
- cd python
- python hand_motor_control.py
