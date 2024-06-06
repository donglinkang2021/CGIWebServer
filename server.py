import socket
import threading
from utils import addr2str
from config import *

# 处理客户端请求
def handle_client(client_socket:socket.socket):
    request = client_socket.recv(1024).decode('utf-8')
    print(f"Received request:\n{request}")
    
    # 创建一个简单的HTTP响应
    response = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n"
    with open('hello.html', 'r') as f:
        response += f.read()
    client_socket.sendall(response.encode('utf-8'))
    client_socket.close()

# 创建服务器套接字
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)
server.listen(MAX_CONN)
server.settimeout(TIMEOUT)
print(f'Server listening on {addr2str(server.getsockname())}')
host_name = socket.gethostbyname(socket.gethostname())
print(f"Server's host name is {host_name}:{PORT}")

# 接受连接
try:
    while True:
        client_sock, addr = server.accept()
        print(f'Accepted connection from {addr}')
        
        # 创建一个新线程来处理请求
        threading.Thread(
            target=handle_client, 
            args=(client_sock,), 
            daemon=True
        ).start()

except KeyboardInterrupt:
    server.close()
    print("\nServer stopped.")
