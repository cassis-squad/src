import logging
import pandas
import time
import os

from scapy.all import *
from threading import Thread


logging.basicConfig(encoding='utf-8', level=logging.DEBUG)

class scan():
    def __init__(self):
       pass
    
    def callback(self, packet):
        pass