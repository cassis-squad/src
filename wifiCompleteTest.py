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
import joblib

from scapy.all import *
from rplidar import RPLidar

LOGGING_FILE = "./log/log-w.log"
logging.basicConfig(filename=LOGGING_FILE, encoding="utf-8", level=logging.DEBUG)

#WIFI MODEL
try:
    model_filename = "lib/wifi_model.joblib"
    with open(model_filename, "rb") as file:
        wifi_m = joblib.load(file)
except FileExistsError:
    logging.critical(f"{datetime.today()} - MODEL NOT FOUND")

global destinazione, actual_pos

class scan():
    def __init__(self):
        self.interface = config.WIFI_INTERFACE_NAME
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
        #obstacle = lidarThread()
        threads = []

        wifi.start()
        lidarThread.start()

        threads.append(wifi)
        #threads.append(obstacle)

        destinazione = input("Inserisci destinazione --> ")
        while True:
                for element in threads:
                        if element.running == False:
                                element.join()
                                print("finish")

if __name__ == "__main__":
        main()