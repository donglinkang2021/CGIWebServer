import socket
import threading

# 配置服务器地址和端口
HOST, PORT = 'localhost', 8888

# 处理客户端请求
def handle_client(client_socket):
    request = client_socket.recv(1024).decode('utf-8')
    print(f"Received request:\n{request}")
    
    # 创建一个简单的HTTP响应
    response = """\
HTTP/1.1 200 OK

<html>
    <head><title>Test Page</title></head>
    <body><h1>Hello, World!</h1></body>
</html>
"""
    client_socket.sendall(response.encode('utf-8'))
    client_socket.close()

# 创建服务器套接字
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(5)
print(f'Server listening on {HOST}:{PORT}')

# 接受连接
try:
    while True:
        client_sock, addr = server.accept()
        print(f'Accepted connection from {addr}')
        
        # 创建一个新线程来处理请求
        client_handler = threading.Thread(target=handle_client, args=(client_sock,))
        client_handler.start()

except KeyboardInterrupt:
    server.close()
    print("\nServer stopped.")
