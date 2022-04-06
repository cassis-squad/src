import logging
from threading import Thread as thr
import time
from datetime import datetime
import pandas as pd
import os
import pickle
import numpy as np
import lib.config as config
import random
import serial
from sklearn import pickle

from scapy.all import *
from rplidar import RPLidar

# LOGGING PLATFORM
LOGGING_FILE = "./log/log.log"
logging.basicConfig(filename=LOGGING_FILE, encoding="utf-8", level=logging.DEBUG)

#WIFI MODEL
try:
    model_filename = "./lib/wifi_model.pkl"
    with open(model_filename, "rb") as file:
        wifi_m = pickle.load(file)
except FileExistsError:
    logging.critical(f"{datetime.today()} - MODEL NOT FOUND")


global destinazione, actual_pos

#! LIDAR CODE

class lidarClass():
    def __init__(self):
        self.arduino = serial.Serial(config.ARDUINO_PORT_NAME ,9600)


    def update_obstacles(self, obstacles, ob):
        for key in ob.keys():
            if ob[key] == True:
                obstacles[key] = True
        return obstacles

    def find_obstacles(self, measurements_list):
        
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

    def avanti(self):
        self.arduino.write(b'0')
        logging.debug(f"{datetime.today()} - GOING FORWARD")

    def stops(self):
        self.arduino.write(b'4')
        logging.debug(f"{datetime.today()} - STOPPED")

    def indietro(self):
        self.arduino.write(b'1')
        logging.debug(f"{datetime.today()} - GOING BACKWARD")

    def destra(self):
        self.arduino.write(b'2')
        logging.debug(f"{datetime.today()} - GOING RIGHT")

    def sinistra(self):
        self.arduino.write(b'3')
        logging.debug(f"{datetime.today()} - GOING LEFT")
        
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

class lidarThread(thr):
        def __init__(self):
                self.running = True
                self.lidar = RPLidar(config.LIDAR_PORT_NAME)
                self.measurments_list = []
                self.lc = lidarClass()
        def run(self):
                for measurment in self.lidar.iter_measurments(max_buf_meas = config.MAX_BUF_MEAS):
                        if destinazione != actual_pos:
                                if self.running == True:
                                        self.measurments_list.append(measurment)
                                        if len(self.measurments_list) >= config.NUMBER_MEASURE:
                                                obstacles = self.lc.find_obstacles(self.measurements_list)
                                                self.lc.motors_controller(obstacles)
                                                obstacles.clear()
                                                self.measurments_list.clear()

                        elif destinazione == actual_pos:
                                self.running = False
                                break

#! WIFI CODE
class scan():
    def __init__(self):
        self.interface = WIFI_INTERFACE_NAME
        self.networks = {'itis-pvt',
                        'itis-wifi',
                        'wifi-itis',
                        'itis-pvt',
                        'itis-wifi2',
                        'AP_SMART25',
                        'wifi-lab01',
                        'AP_ITISLI03_2.5',
                        'AP_SMART50',
                        'AP_ITISLI03_5.0',
                        'AP_ITISLI02'}
        self.net_dict = {}

    def callback(self, packet):
        if packet.haslayer(Dot11Beacon):
            # get the name of it
            ssid = packet[Dot11Elt].info.decode()
            try:
                dbm_signal = packet.dBm_AntSignal
            except:
                dbm_signal = "N/A"
            if ssid in self.newtorks:
                self.net_dict[ssid] = dbm_signal

    def wifi(self):
        self.net_dict = {i : None for i in self.networks}
        sniff(prn=self.callback, iface=self.interface, count=100)
        lan = []
        for net in self.newtorks:
            if self.net_dict[net] is None:
                lan.append("-120")
            else: 
                lan.append(self.net_dict[net])
        
        lan = np.array(lan)
        return lan

    def wifiPositioning(self):
        actual_scan = self.wifi()
        actual_pos = wifi_m.predict(actual_scan)

        return actual_pos

class wifiThread(thr):
        def __init__(self):
                self.running = True
                self.TIME = 30
                self.scan = scan()

        def run(self):
                global destinazione, actual_pos
                if destinazione != actual_pos:
                        if self.running == True:
                                time.sleep(self.TIME)
                                actual_pos = self.scan.wifiPositioning(destinazione)
                                logging.debug(f"{datetime.today()} - SCAN")
                elif destinazione == actual_pos:
                        self.running = False
                        logging.debug(f"{datetime.today()} - EXITING SCAN THREAD")

def main():
        global destinazione

        wifi = wifiThread()
        obstacle = lidarThread()
        threads = []

        wifi.start()
        lidarThread.start()

        threads.append(wifi)
        threads.append(obstacle)

        destinazione = input("Inserisci destinazione --> ")
        while True:
                for element in threads:
                        if element.running == False:
                                element.join()
                                print("finish")

if __name__ == "__main__":
        main()