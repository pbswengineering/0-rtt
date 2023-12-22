import os

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

from scapy.all import *
from scapy.utils import rdpcap
from scapy.layers.tls import *
import random

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
app_data_full = None
for p in pkts:
     if p.getlayer(TLSClientHello):
          client_hello_full = p
     if p.getlayer(TLSApplicationData):
          app_data_full = p

ip = IP(dst='127.0.0.1')
sport = random.randint(14344, 15843)
#sport = client_hello_full.getlayer(TCP).sport
print("sport =", sport)
input("Press ENTER to continue...")

### Three-way TCP handshake
print("   ---> SYN...")
syn = ip / TCP(dport=443, sport=sport, flags='S', seq=1000)
syn_ack = sr1(syn)
print("ACK...")
ack = TCP(sport=syn.sport, dport=443, flags='A', seq=syn_ack.ack, ack=syn_ack.seq + 1)
ack_resp = sr1(ip/ack)

### Business
print("   ---> 0-RTT request")
request = ip \
            / TCP(sport=syn.sport, dport=443, flags='A', seq=ack_resp.ack, ack=ack_resp.seq + 1) \
            / client_hello_full.getlayer(TLS)
#request.show()
ans, unans = sr(request)
ans.summary()
tls_resp = ans[0][0]
ack_resp = ans[0][1]

print("   ---> ACK...")
request = ip \
            / TCP(sport=syn.sport, dport=443, flags='A', seq=ack_resp.ack, ack=ack_resp.seq + 1)
#request.show()
ans, unans = sr(request)
ans.summary()

print("   ---> APP DATA....")
request = ip \
            / TCP(sport=syn.sport, dport=443, flags='A', seq=ack_resp.ack, ack=ack_resp.seq + 1) \
            / app_data_full.getlayer(TLS)
#request.show()
ans, unans = sr(request)
ans.summary()
ack_resp = ans[0][1]

print("   ---> FIN...")
request = ip \
            / TCP(sport=syn.sport, dport=443, flags='FA', seq=ack_resp.ack, ack=ack_resp.seq + 1)
#request.show()
ans, unans = sr(request)
ans.summary()
