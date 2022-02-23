import logging
import pandas
import time
import os

from scapy.all import *
from threading import Thread


logging.basicConfig(encoding='utf-8', level=logging.DEBUG)

class scan():
    def __init__(self):
        self.networks = pandas.DataFrame(columns=["BSSID", "SSID", "dBm_Signal", "Channel", "Crypto"])
        self.networks.set_index("BSSID", inplace=True)
        logging.debug("Dataframe setup complete")
    
    def callback(self, packet):
        if packet.hasLayer(Dot11Beacon):
            bssid = packet[Dot11].addr2
            ssid = packet[Dot11Elt].info.decode()

            try:
                dbm_signal = packet.dBm_AntSignal
                logging.debug("Gathered signal")
            except:
                dbm_signal = "N/A"
                logging.debug("Ungathered signal")

            stats = packet[Dot11Beacon].network_stats()
            channel = stats.get("channel")
            crypto = stats.get("crypto")
            networks.loc[bssid] = (ssid, dbm_signal, channel, crypto)
