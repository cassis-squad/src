import logging
from datetime import datetime

import serial

# 0 --> Avanti
# 1 --> Indietro
# 2 --> Destra
# 3 --> Sinistra

# A --> piano
# B --> medio
# C --> veloce

logging.basicConfig(encoding="utf-8", level=logging.DEBUG)

class ArduinoCommands:
    def __init__(self):
        USB_PORT = "/dev/ttyACM0"

    def connectionTest(self):
        usb = None
        try:
            usb = serial.Serial(self.USB_PORT, 9600, timeout=2)
        except:
            logging.critical(f"{datetime.today()} USB CONNECTION FAILED")
            exit()

        return usb

    def control(self, command):
        usb = self.connectionTest()

        if command == "0":
            usb.write(b"0")
            logging.debug("Send forward to Arduino --> 0")
        elif command == "1":
            usb.write(b"1")
            logging.debug("Send backward to Arduino --> 1")
        elif command == "2":
            usb.write(b"2")
            logging.debug("Send right to Arduino --> 2")
        elif command == "3":
            usb.write(b"3")
            logging.debug("Send left to Arduino --> 3")
        else:
            logging.warning("Command not recognized! -- 404")

    def speedControl(self, speed):
        usb = self.connectionTest()

        if speed == "A":
            usb.write(b"A")
            logging.debug("Send low speed to Arduino")
        elif speed == "B":
            usb.write(b"B")
            logging.debug("Send mid speed to Arduino")
        elif speed == "C":
            usb.write(b"C")
            logging.debug("Send high speed to Arduino")
        else:
            logging.warning("Speed not recognized! -- 404")
