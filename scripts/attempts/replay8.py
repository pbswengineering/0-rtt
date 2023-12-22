from http.server import HTTPServer, SimpleHTTPRequestHandler
import ssl


httpd = HTTPServer(('localhost', 443), SimpleHTTPRequestHandler)

httpd.socket = ssl.wrap_socket (httpd.socket, 
        keyfile="../containers/ca/localhost_key.pem", 
        certfile="../containers/ca/localhost.crt", server_side=True)

httpd.serve_forever()