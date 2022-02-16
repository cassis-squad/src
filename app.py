import logging
from lib.arduino.commandToArduino import ArduinoCommands
from lib.lidar.lidarObjectModel import *
from lib.wifi.wifiScan import *

# LOGGING PLATFORM
LOGGING_FILE = "./log/log.log"
logging.basicConfig(filename=LOGGING_FILE, encoding='utf-8', level=logging.DEBUG)

class main():
    def __init__(self):
        self.arduino = ArduinoCommands()

    def control(self):
        usb = self.arduino.control()        

m = main()