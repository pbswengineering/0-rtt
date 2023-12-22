import socket
from tls import TLSClientSession

quit = False
sock = None

def callback(data):
    global quit, sock
    print(data)
    if data == b"bye\n":
        quit = True

psk = bytes.fromhex(
    "b2c9b9f57ef2fbbba8b624070b301d7f278f1b39c352d5fa849f85a3e7a3f77b"
)
session = TLSClientSession(
    server_names="127.0.0.1", 
    psk=psk, 
    data_callback=callback, 
    psk_only=True, 
    early_data=b"GET / HTTP/1.1\r\nHost: 127.0.0.1\r\n\r\n"
)
#session = TLSClientSession(server_names="127.0.0.1", data_callback=callback)
quit = False
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("127.0.0.1", 443))
sock.sendall(session.pack_client_hello())

parser = session.parser()
server_data = sock.recv(409600)
parser.send(server_data)
data = parser.read()
if data:
    sock.sendall(data)

sock.sendall(session.pack_close())
sock.close()