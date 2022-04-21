import time
import sys
import config
import serial
import random
from rplidar import RPLidarù
import logging
from datetime import datetime

# 0 --> Avanti
# 1 --> Indietro
# 2 --> Destra
# 3 --> Sinistra
# 4 --> Stop

# A --> piano
# B --> medio
# C --> veloce

arduino = serial.Serial(config.ARDUINO_PORT_NAME ,9600)
logging.basicConfig(filename=LOGGING_FILE, encoding="utf-8", level=logging.DEBUG)


def update_obstacles(obstacles, ob):
    for key in ob.keys():
        if ob[key] == True:
            obstacles[key] = True
    return obstacles

def find_obstacles(measurements_list):
    
    ret_dict= {"left": False, "center": False, "right": False}
    
    for measure_tuple in measurements_list:
        
        ob_dict = {"left": False, "center": False, "right": False}
        
        measure_bool, measure_power, measure_angle, measure_distance = measure_tuple
        
        if measure_distance <= config.MAX_DISTANCE and measure_distance >= config.MIN_DISTANCE and measure_power >= config.QUALITY:
            #right
            if measure_angle > config.RIGHT / 2 and measure_angle <= config.RIGHT:
                ob_dict["right"] = True
            #left
            elif measure_angle >= config.LEFT and measure_angle < (360 -(config.RIGHT/2)):
                ob_dict["left"] = True
            #center
            elif measure_angle >= config.CENTER and measure_angle <= config.RIGHT/2:
                ob_dict["center"] = True
            #center
            elif measure_angle >= (360 -(config.RIGHT/2)) and measure_angle <= 360:
                ob_dict["center"] = True
        
            ret_dict = update_obstacles(ret_dict, ob_dict)
        
    return ret_dict

def avanti():
    arduino.write(b'0')
    logging.debug(f"{datetime.today()} - GOING FORWARD")

def stops():
    arduino.write(b'4')
    logging.debug(f"{datetime.today()} - STOPPED")

def indietro():
    arduino.write(b'1')
    logging.debug(f"{datetime.today()} - GOING BACKWARD")

def destra():
    arduino.write(b'2')
    logging.debug(f"{datetime.today()} - GOING RIGHT")

def sinistra():
    arduino.write(b'3')
    logging.debug(f"{datetime.today()} - GOING LEFT")
    
def random_directions():
    direction_list = [sinistra(), destra()]
    direction = random.choice(direction_list)
    direction

def motors_controller(obstacles):
    if obstacles["center"] == False:
        avanti()
    elif obstacles["left"] == True:
        if obstacles["right"] == True:
            stops()
            random_directions()
            time.sleep(3)
        else:
            destra()
            time.sleep(1)
    elif obstacles["right"] == True:
        if obstacles["left"] == True:
            stops()
            random_directions()
            time.sleep(3)
        else:
            sinistra()
            time.sleep(1)
    else:
        stops()
        random_directions()

def main():
    lidar = RPLidar(config.LIDAR_PORT_NAME)
    time.sleep(5)
    measurments_list = []

    try:
        for measurment in lidar.iter_measurments(max_buf_meas = config.MAX_BUF_MEAS):
             measurments_list.append(measurment)
             if len(measurments_list) >= config.NUMBER_MEASURE:
                obstacles = find_obstacles(measurments_list)
                motors_controller(obstacles)
                obstacles.clear()
                measurments_list.clear()
                
    except KeyboardInterrupt:
        lidar.stop()
        lidar.stop_motor()
        lidar.disconnect()
        stops()