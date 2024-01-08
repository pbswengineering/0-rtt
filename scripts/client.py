from sslyze.server_connectivity import *
from sslyze.errors import *
from sslyze.connection_helpers.http_request_generator import *
from nassl._nassl import OpenSSLError
from nassl.ssl_client import OpenSslEarlyDataStatusEnum, SslClient
from termcolor import colored

target_host = "127.0.0.1"
target_port = 4443

w = lambda s: colored(s, "white")
cb = lambda s: colored(s, "cyan", attrs=['bold'])
rb = lambda s: colored(s, "red", attrs=['bold'])
gb = lambda s: colored(s, "green", attrs=['bold'])

#receiver = "test"
#amount = 50
print(cb("Receiver: "), end="")
receiver = input()
print(cb("Amount: "), end="")
amount = int(input())

print(w("Target server:"), cb(target_host) + w(":") + cb(target_port))
server_location = ServerNetworkLocation(target_host, target_port)
network_configuration = ServerNetworkConfiguration(target_host)
tls_probing_result = ServerTlsProbingResult(
    TlsVersionEnum.TLS_1_3,
    "TLS_AES_256_GCM_SHA384",
    ClientAuthRequirementEnum.DISABLED,
    True)
server_info = ServerConnectivityInfo(server_location, network_configuration, tls_probing_result)
session = None
is_early_data_supported = False
print(w("Performing"), gb("complete"), w("TLS handshake..."))
ssl_connection = server_info.get_preconfigured_tls_connection(override_tls_version=TlsVersionEnum.TLS_1_3)
# Perform an SSL handshake and keep the session
ssl_connection.connect()
# Send and receive data for the TLS session to be created
ssl_connection.ssl_client.write(HttpRequestGenerator.get_request(host=server_info.server_location.hostname))
ssl_connection.ssl_client.read(2048)
session = ssl_connection.ssl_client.get_session()
ssl_connection.close()

# Then try to re-use the session and send early data
if session is not None:
    ok = False
    try:
        print(w("Performing"), rb("0-RTT"), w("TLS handshake..."))
        ssl_connection2 = server_info.get_preconfigured_tls_connection(override_tls_version=TlsVersionEnum.TLS_1_3)
        if not isinstance(ssl_connection2.ssl_client, SslClient):
            raise RuntimeError("Should never happen")

        ssl_connection2.ssl_client.set_session(session)

        # Open a socket to the server but don't do the actual TLS handshake
        ssl_connection2._do_pre_handshake()

        # Send some bytes of early data
        ssl_connection2.ssl_client.write_early_data(f"GET /index.php?receiver={receiver}&amount={amount} HTTP/1.1\r\nHost: 127.0.0.1\r\n\r\n".encode())
        ssl_connection2.ssl_client.do_handshake()
        if ssl_connection2.ssl_client.get_early_data_status() == OpenSslEarlyDataStatusEnum.ACCEPTED:
            print(gb("Transfer completed, early data is supported"))
        else:
            print(rb("Early data is NOT supported"))
        ssl_connection2.close()
        ok = True
    except:
        print("Connection error, retrying in 1 second...")
        import time
        time.sleep(5)