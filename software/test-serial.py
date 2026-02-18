# port connection test. not required!

import serial
import time

esp = serial.Serial('/dev/cu.usbmodem14101', 115200)
time.sleep(2)  

while True:
    cmd = input("Type ON or OFF: ")
    esp.write((cmd + "\n").encode())
