import logging
from threading import Thread as thr
import time
from datetime import datetime
import os
import numpy as np
import lib.config as config
import random
import serial
from rplidar import RPLidar

LOGGING_FILE = "./log/log-l.log"
logging.basicConfig(filename=LOGGING_FILE, encoding="utf-8", level=logging.DEBUG)

global destinazione, actual_pos
actual_pos="prova"

class lidarClass():
    def __init__(self):
        pass
        #self.arduino = serial.Serial(config.ARDUINO_PORT_NAME ,9600)


    def find_obstacles(self, measurements_list):
        
        ret_dict= {"left": False, "center": False, "right": False}
        
        for measure_tuple in measurements_list:
            
            ob_dict = {"left": False, "center": False, "right": False}
            
            measure_bool, measure_power, measure_angle, measure_distance = measure_tuple
            
            if measure_distance <= config.MAX_DISTANCE and measure_distance >= config.MIN_DISTANCE and measure_power >= config.QUALITY:
                #right
                if measure_angle < 135 and measure_angle > 90:
                    ob_dict["right"] = True
                    print(ob_dict)
                #left
                elif measure_angle > 315 and measure_angle < 300:
                    ob_dict["left"] = True
                    print(ob_dict)
                #center
                elif measure_angle < 90:
                    ob_dict["center"] = True
                    print(ob_dict)
            
                ret_dict = update_obstacles(ret_dict, ob_dict)
            
        return ret_dict

    def avanti(self):
        self.arduino.write(b'w')
        logging.debug(f"{datetime.today()} - GOING FORWARD")
        print("avanti")

    def stops(self):
        self.arduino.write(b'q')
        logging.debug(f"{datetime.today()} - STOPPED")
        print("stop")

    def indietro(self):
        self.arduino.write(b's')
        logging.debug(f"{datetime.today()} - GOING BACKWARD")
        print("indietro")

    def destra(self):
        self.arduino.write(b'd')
        logging.debug(f"{datetime.today()} - GOING RIGHT")
        print("destra")

    def sinistra(self):
        self.arduino.write(b'a')
        logging.debug(f"{datetime.today()} - GOING LEFT")
        print("sinistra")

    def random_directions(self):
        direction_list = [self.sinistra(), self.destra()]
        direction = random.choice(direction_list)
        direction

    def motors_controller(self, obstacles):
        if obstacles["center"] == False:
            self.avanti()
        elif obstacles["left"] == True:
            if obstacles["right"] == True:
                self.stops()
                self.random_directions()
                time.sleep(3)
            else:
                self.destra()
                time.sleep(1)
        elif obstacles["right"] == True:
            if obstacles["left"] == True:
                self.stops()
                self.random_directions()
                time.sleep(3)
            else:
                self.sinistra()
                time.sleep(1)
        else:
            self.stops()
            self.random_directions()

class lidarThread():
        def __init__(self):
                self.running = True
                self.lidar = RPLidar(config.LIDAR_PORT_NAME)
                self.measurments_list = []
                self.lc = lidarClass()
        def run(self):
            iterator = self.lidar.iter_scans()
            for measurment in self.lidar.iter_scans(max_buf_meas = config.MAX_BUF_MEAS):
                    if destinazione != actual_pos:
                            if self.running == True:
                                    self.measurments_list.append(measurment)
                                    if len(self.measurments_list) >= config.NUMBER_MEASURE:
                                            obstacles = self.lc.find_obstacles(self.measurements_list)
                                            print(obstacles)
                                            self.lc.motors_controller(obstacles)
                                            obstacles.clear()
                                            self.measurments_list.clear()

                    elif destinazione == actual_pos:
                            self.running = False
                            break

def main():
        global destinazione

        lidarThread.run()

        #wifi = wifiThread()
        '''
        obstacle = lidarThread()
        threads = []

        destinazione = "test"

        #wifi.start()
        obstacle.start()

        #threads.append(wifi)
        threads.append(obstacle)

        while True:
                for element in threads:
                        if element.running == False:
                                element.join()
                                print("finish")
        '''

if __name__ == "__main__":
        main()