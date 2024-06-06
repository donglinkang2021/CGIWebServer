import os
import socket
import threading
from config import *

def send_response(client:socket.socket, status_code:int):
    status_str = f"{status_code} {HTTP_RESPONSES[status_code]}"
    response = f"HTTP/1.1 {status_str}\r\nContent-Type: text/html\r\n\r\n"
    client.sendall(response.encode('utf-8'))

def send_file(client:socket.socket, file_path:str):
    if not os.path.exists(file_path):
        send_response(client, 404)
    else:
        send_response(client, 200)
        file_bytes = open(file_path, 'rb')
        for line in file_bytes:
            client.sendall(line)

class HTTPServer:
    def __init__(self, host:str, port:int, max_conn:int, timeout:int):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((host, port))
        self.server.listen(max_conn)
        self.server.settimeout(timeout)
        self.host_name = socket.gethostbyname(socket.gethostname())
        print(f"Server root: http://{self.host_name}:{port}/")

    def run(self):
        try:
            while True:
                client, addr = self.server.accept()
                print(f'Accepted connection from {addr}')
                threading.Thread(
                    target=self.handle_client, 
                    args=(client,), 
                    daemon=True
                ).start()

        except KeyboardInterrupt:
            self.server.close()
            print("\nServer stopped.")

    def handle_client(self, client:socket.socket):
        request = client.recv(1024).decode('utf-8')
        print(f"Received request:\n{request}")
        send_file(client, "hello.html")
        client.close()

if __name__ == '__main__':
    server = HTTPServer(HOST, PORT, MAX_CONN, TIMEOUT)
    server.run()