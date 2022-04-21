from scapy.all import *
from threading import Thread
import time
import os
import numpy as np
from joblib import load

model_filename = "/home/rdfilippo/Desktop/Scuola/PON-CassisSquad/src/lib/wifi_model.joblib"
wifi_m = load(model_filename)


class scan():
    def __init__(self):
        self.interface = "wlan1mon"
        self.networks = {'itis-pvt',
                        'itis-wifi',
                        'itis-pvt',
                        'itis-wifi2',
                        'wifi-itis',
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
            if ssid in self.networks:
                self.net_dict[ssid] = dbm_signal

    def wifi(self):
        self.net_dict = {i : None for i in self.networks}
        sniff(prn=self.callback, iface=self.interface, count=100)
        lan = []
        for net in self.networks:
            if self.net_dict[net] is None:
                lan.append("-120")
            else:
                lan.append(self.net_dict[net])

        lan = np.array([lan])
        return lan

    def predict(self):
        testLect = self.wifi()
        print(testLect)
        print(wifi_m.predict(testLect))



if __name__ == "__main__":
    test = scan()
    test.predict()
