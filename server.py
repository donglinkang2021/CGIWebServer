import os
import socket
import threading
from config import *
from myhttp import get_status_str, get_content_type
import subprocess
import urllib.parse
from typing import Tuple

def send_response(client: socket.socket, status_code: int, content_type='text/html', body=b''):
    response = f"HTTP/1.1 {get_status_str(status_code)}\r\nContent-Type: {content_type}\r\n\r\n"
    client.sendall(response.encode('utf-8') + body)

def send_error(client: socket.socket, status_code: int):
    error_path = DOCUMENT_ROOT + '/info.html'
    body = open(error_path, 'r', encoding='utf-8').read()
    body = body.replace('info', get_status_str(status_code)).encode('utf-8')
    send_response(client, status_code, body=body)

def send_file(client: socket.socket, file_path: str):
    if not os.path.exists(file_path):
        send_error(client, 404)
    else:
        body = open(file_path, 'rb').read()
        content_type = get_content_type(file_path)
        send_response(client, 200, content_type, body)

def execute_cgi(client: socket.socket, path: str, method: str, body: str):
    if not os.path.exists(DOCUMENT_ROOT + path):
        send_error(client, 404)
        return
    
    env = os.environ.copy()
    env['REQUEST_METHOD'] = method
    env['CONTENT_LENGTH'] = str(len(body))

    process = subprocess.Popen(
        ['python', f'.{path}'],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=DOCUMENT_ROOT,
        env=env,
    )

    stdout, stderr = process.communicate(input=body.encode('utf-8'))
    if process.returncode != 0:
        send_error(client, 500)
        print(stderr.decode('utf-8'))
    else:
        send_response(client, 200, 'text/html', stdout)

def get_headers_body(request: str) -> Tuple[dict, str]:
    headers = {}
    body = ''
    if '\r\n\r\n' in request:
        headers_body = request.split('\r\n\r\n', 1)
        headers = dict([line.split(': ', 1) for line in headers_body[0].splitlines()[1:]])
        body = headers_body[1]
    return headers, body

class HTTPServer:
    def __init__(self, host: str, port: int, max_conn: int, timeout: int):
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
    
    def handle_GET(self, client: socket.socket, path: str):
        if path == '/':
            path = '/index.html'
        file_path = DOCUMENT_ROOT + path
        send_file(client, file_path)

    def handle_POST(self, client: socket.socket, path: str, body: str):
        if path.startswith('/cgi-bin/'):
            execute_cgi(client, path, 'POST', body)
        else:
            send_error(client, 404)

    def handle_client(self, client: socket.socket):
        try:
            request = client.recv(1024).decode('utf-8')
            request_line = request.splitlines()[0]
            request_method, path, http_version = request_line.split()
            print(f"request method: {request_method}, path: {path}, version: {http_version}")

            if request_method == 'GET':
                self.handle_GET(client, path)
            elif request_method == 'POST':
                _, body = get_headers_body(request)
                self.handle_POST(client, path, body)
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