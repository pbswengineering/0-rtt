import os

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

from scapy.all import *
from scapy.utils import rdpcap
from scapy.layers.tls import *
import random
import socket
import sys

load_layer("http")
load_layer("tls")

# See https://scapy.readthedocs.io/en/latest/troubleshooting.html
conf.L3socket = L3RawSocket

# Remember, to avoid unwanted RST from Linux
# iptables -A OUTPUT -p tcp --tcp-flags RST RST -s 127.0.0.1 -j DROP

# Wireshark filter
# tcp.srcport == 443 || tcp.dstport == 443

pkts = rdpcap("/home/rnd/Downloads/sslyze.pcapng")
client_hello_full = None
app_data_full = []
collect_app_data = False
for p in pkts:
     if p.getlayer(TLSClientHello):
          client_hello_full = p
          collect_app_data = True
     elif p.getlayer(TLSApplicationData) and collect_app_data:
          app_data_full.append(p)

target = ('127.0.0.1', 443)
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect(target)

### Business
print("   ---> 0-RTT request")
s.sendall(bytes(client_hello_full.getlayer(TLS)))
resp = s.recv(1024)
print("Resp:", repr(resp))

print("   ---> APP DATA....")
print(len(app_data_full))
for p in app_data_full:
     s.sendall(bytes(p.getlayer(TLS)))
     resp = s.recv(1024)
     print("Resp:", repr(resp))
#TLS(resp).show()
#input("Wait...")

s.close()