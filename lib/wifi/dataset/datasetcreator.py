'''
Use conditions:
    -network adapter settled in Monitor mode
    -the device can't be connected to a network
'''

from scapy.all import *
from threading import Thread
import pandas
import time
import os


# interface name, check using iwconfig
N_TIMES = 30
interface = "wlan0mon"
zone = -1
newtorks = {'itis-pvt',
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
net_dict = {}

def callback(packet):
    if packet.haslayer(Dot11Beacon):
        # get the name of it
        ssid = packet[Dot11Elt].info.decode()
        try:
            dbm_signal = packet.dBm_AntSignal
        except:
            dbm_signal = "N/A"
        if ssid in newtorks:
            net_dict[ssid] = dbm_signal

def main():     
    global zone
    global net_dict

    with open('./dataset.csv','w') as fp:
        fp.write('macro_zone, micro_zone,')
        for net in newtorks:
            fp.write(f'{net},')
        fp.write('\n')

    while True:
        macro_zone = input('Insert the macro-zone: ')
        micro_zone = input('Insert the micro-zone: ')
        for _ in range(N_TIMES):
            net_dict = {i : None for i in newtorks}
            sniff(prn=callback, iface=interface, count=100)
            with open('./dataset.csv','a') as fp:
                fp.write(f'{macro_zone},{micro_zone},')
                for net in newtorks:
                    if net_dict[net] is None:
                        fp.write('-120,')
                    else: 
                        fp.write(f'{net_dict[net]},')    
                fp.write('\n')
        
        

if __name__ == "__main__":
    main()