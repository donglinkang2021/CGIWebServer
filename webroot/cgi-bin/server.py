import socket
import json

server_name = socket.gethostname()
server_address = socket.gethostbyname(server_name)

info = {
    "serverName": server_name,
    "serverAddress": server_address
}

content = json.dumps(info)
content_length = len(content)

head = "HTTP/1.1 200 OK\n"
head += "Content-Type: application/json\n"
head += f"Content-Length: {content_length}\n\n"
print(head + content)
