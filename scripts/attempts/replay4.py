print("Parsing packet data...")
import pyshark
cap = pyshark.FileCapture(
    input_file="/home/rnd/Downloads/sslyze.pcapng",
    use_json=True,
    include_raw=True
)
zero_rtt = cap[36]
#print(zero_rtt)

print("TCP handshake")
from scapy.all import *
from scapy.utils import rdpcap
from scapy.layers.tls import *
import random
# See https://scapy.readthedocs.io/en/latest/troubleshooting.html
conf.L3socket = L3RawSocket
ip = IP(dst='127.0.0.1')
#sport = random.randint(14344, 15843)
sport = int(zero_rtt.tcp.srcport)
print("SYN...")
syn = ip / TCP(dport=443, sport=sport, flags='S', seq=1000)
syn_ack = sr1(syn)
print("ACK...")
ack = TCP(sport=syn.sport, dport=443, flags='A', seq=syn_ack.ack, ack=syn_ack.seq + 1)
ack_resp = sr1(ip/ack)

print("Packet reply")
from socket import socket, AF_PACKET, SOCK_RAW
sock = socket(AF_PACKET, SOCK_RAW)
sock.bind(('lo', 0))
raw_bytes = bytearray.fromhex(zero_rtt.frame_raw.value)
print(raw_bytes)
sock.send(raw_bytes)