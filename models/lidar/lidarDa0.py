from rplidar import RPLidar
import numpy as np
import time
import random
import serial
import time

PORT_NAME = '/dev/ttyUSB0'
arduino = serial.Serial('/dev/ttyACM0' ,9600)
DMAX = 4000
IMIN = 0
IMAX = 50

global tempo
tempo = 10000

def avanti():
    arduino.write(b'w')
    #logging.debug(f"{datetime.today()} - GOING FORWARD")
    print("avanti")

def stops():
    arduino.write(b'q')
    #logging.debug(f"{datetime.today()} - STOPPED")
    #print("stop")

def indietro():
    arduino.write(b's')
    #logging.debug(f"{datetime.today()} - GOING BACKWARD")
    print("indietro")

def destra():
    arduino.write(b'd')
    #logging.debug(f"{datetime.today()} - GOING RIGHT")
    print("destra")
def sinistra():
    arduino.write(b'a')
    #logging.debug(f"{datetime.today()} - GOING LEFT")
    print("sinistra")

def Oavanti():
    r = random.randint(0, 1)
    if r == 0:
        destra()
    else:
        sinistra()


def run():

    global tempo

    movements = {
        "right" : False,
        "left" : False,
        "center" : False
    }
    i = 0

    try: 
        lidar = RPLidar(PORT_NAME)

        iterator = lidar.iter_scans(max_buf_meas=400, min_len=0)
        for element in iterator:
            for e in element:
                if e[0] > 13:
                    if e[1] > 300 or e[1] < 150:
                        #q = int(e[0])
                        #a = e[1]
                        #d = e[2] / 1000
                        if e[1] < 90 and e[2] < 300:
                            movements["center"] = True
                            movements["right"] = False
                            movements["left"] = False
                        elif e[1] > 90 and e[1] < 135 and e[2] < 300:
                            movements["center"] = False
                            movements["right"] = True
                            movements["left"] = False
                        elif e[1] > 315 and e[2] < 300:
                            movements["center"] = False
                            movements["right"] = False
                            movements["left"] = True
                        else:
                            movements["center"] = False
                            movements["right"] = False
                            movements["left"] = False
                            #print("libero")
                        
                        if movements["center"] == True:
                            stops()
                            Oavanti()
                        elif movements["right"] == True:
                            stops()
                            sinistra()
                        elif movements["left"] == True:
                            stops()
                            destra()
                        elif movements["center"] == False and movements["right"] == False and movements["left"] == False:
                            stops()
                            avanti()
                        #print(f"angolo: {a}")
                        #print(f"distanza: {d}")
                    
                        #time.sleep(0.2)
    
        lidar.stop()
        lidar.disconnect()
    except KeyboardInterrupt:
        lidar.stop()
        lidar.disconnect()

if __name__ == '__main__':
    run()