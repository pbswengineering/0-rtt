import os
import random

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

from scapy.all import *
from scapy.utils import rdpcap
from scapy.layers.tls import *
import socket

target = ("localhost", 443)

load_layer("tls")

pkts = rdpcap("/home/rnd/Downloads/sslyze.pcapng")
zero_rtt = pkts[36]
zero_rtt.show()