import cgi
import socket
import json

server_name = socket.gethostname()
server_address = socket.gethostbyname(server_name)

info = {
    "serverName": server_name,
    "serverAddress": server_address
}
print("Content-Type: application/json\n")
print(json.dumps(info))
