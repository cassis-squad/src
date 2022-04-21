import logging
import pandas
import time
import os
import pickle
import numpy as np
from datetime import datetime
from threading import Thread


logging.basicConfig(encoding='utf-8', level=logging.DEBUG)

#model
model_filename = "modello/wifi_model.pkl"
with open(model_filename, "rb") as file:
    wifi_m = pickle.load(file)


class scan():
    def __init__(self):
        self.interface = "wlan1mon"
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
        lan = np.array([[]])
        for net in self.newtorks:
            if self.net_dict[net] is None:
                np.append(lan, "-120")
            else: 
                np.append(lan,self.net_dict[net])
        
        return lan

    def wifiPositioning(self, destinazione):
        actual_scan = self.wifi()
        actual_pos = wifi_m.predict(actual_scan)

        if actual_pos == destinazione:
            return actual_pos
        else:
            return "-1"
        