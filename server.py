import os
import socket
import threading
from config import *
from myhttp import get_status_str, get_content_type

def send_response(client:socket.socket, status_code:int, content_type='text/html', body=b''):
    response = f"HTTP/1.1 {get_status_str(status_code)}\r\nContent-Type: {content_type}\r\n\r\n"
    client.sendall(response.encode('utf-8') + body)

def send_error(client:socket.socket, status_code:int):
    error_path = DOCUMENT_ROOT + '/info.html'
    body = open(error_path, 'r', encoding='utf-8').read()
    body = body.replace('info', get_status_str(status_code)).encode('utf-8')
    send_response(client, status_code, body=body)

def send_file(client:socket.socket, file_path:str):
    if not os.path.exists(file_path):
        send_error(client, 404)
    else:
        body = open(file_path, 'rb').read()
        content_type = get_content_type(file_path)
        send_response(client, 200, content_type, body)

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
    
    def handle_GET(self, client:socket.socket, path:str):
        if path == '/':
            path = '/index.html'
        file_path = DOCUMENT_ROOT + path
        send_file(client, file_path)

    def handle_client(self, client:socket.socket):
        try:
            request = client.recv(1024).decode('utf-8')
            request_line = request.splitlines()[0]
            request_method, path, http_version = request_line.split()
            print(f"request method: {request_method}, path: {path}, version: {http_version}")

            if request_method == 'GET':
                self.handle_GET(client, path)
            else:
                send_error(client, 400)

        except Exception as e:
            print(f"Error handling client: {e}")
            send_error(client, 500)
        finally:
            client.close()

if __name__ == '__main__':
    server = HTTPServer(HOST, PORT, MAX_CONN, TIMEOUT)
    server.run()