import logging
from lib.commandToArduino import ArduinoCommands

# LOGGING PLATFORM
LOGGING_FILE = "log.log"
logging.basicConfig(filename=LOGGING_FILE, encoding='utf-8', level=logging.DEBUG)

class main():
    def __init__(self):
        self.arduino = ArduinoCommands()

    def control(self):
        usb = self.arduino.control()        

m = main()