from scapy.all import *
from scapy.utils import rdpcap
from scapy.layers.tls import *
import socket
import random

load_layer("http")
load_layer("tls")

# See https://scapy.readthedocs.io/en/latest/troubleshooting.html
conf.L3socket = L3RawSocket

# Remember, to avoid unwanted RST from Linux
# iptables -A OUTPUT -p tcp --tcp-flags RST RST -s 127.0.0.1 -j DROP

# Wireshark filter
# tcp.srcport == 443 || tcp.dstport == 443

### TCP 3-way handshake

ip = IP(dst='127.0.0.1')
sport = random.randint(14344, 15843)

print("SYN...")
syn = ip / TCP(dport=443, sport=sport, flags='S', seq=1000)
syn_ack = sr1(syn)
print("ACK...")
ack = TCP(sport=syn.sport, dport=443, flags='A', seq=syn_ack.ack, ack=syn_ack.seq + 1)
ack_resp = sr1(ip/ack)

### Business

pkts = rdpcap("/home/rnd/Downloads/sslyze.pcapng")
zero_rtt = pkts[120]

tls1 = zero_rtt.getlayer(TLSClientHello)
tls2 = zero_rtt.getlayer(TLSChangeCipherSpec)
tls3 = zero_rtt.getlayer(TLSApplicationData)

#getStr = 'GET / HTTP/1.1\r\nHost: 127.0.0.1\r\n\r\n'
request = ip \
            / TCP(sport=syn.sport, dport=443, flags='A', seq=ack_resp.ack, ack=ack_resp.seq) \
            / TLS(tls1).load \
            / TLS(tls2).load \
            / TLS(tls3).load
request.show()
reply = sr1(request)
reply.show()
print(type(reply.getlayer(TCP).payload))
