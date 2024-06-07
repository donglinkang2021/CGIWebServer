import os
import subprocess
import threading
import socket
import json
from .header import Header
from .status import get_status_str
from .utils import *

__all__ = ['RequestHandler']

class RequestHandler(threading.Thread):
    def __init__(self, 
            client: socket.socket, 
            address: tuple,
            work_dir: str,
            http_version: str,
            *args, **kwargs
        ):
        super().__init__(*args, **kwargs)
        self.client = client
        self.address = address
        self.work_dir = work_dir
        self.http_version = http_version
        # use for error page
        self.info_page_path = self.work_dir + '/info.html'

    def send_response(self, head = b'', body=b''):
        self.client.sendall(head + body)
    
    def send_error(self, status_code: int):
        body = open(self.info_page_path, 'r', encoding='utf-8').read()
        body = body.replace('info', get_status_str(status_code)).encode('utf-8')
        head = Header(self.http_version, status_code)\
            .add_header('Content-Type', 'text/html')\
            .__str__().encode('utf-8')
        self.send_response(head, body)

    def send_file(self, path: str, just_head=False):
        if path == '/':
            path = '/index.html'
        file_path = self.work_dir + path
        if not os.path.exists(file_path):
            self.send_error(404)
        else:
            body = open(file_path, 'rb').read()
            content_type = get_content_type(file_path)
            head = Header(self.http_version, 200)\
                .add_header('Content-Type', content_type)\
                .add_header('Content-Length', str(len(body)))\
                .add_header('Last-Modified', date_time_string())\
                .__str__().encode('utf-8')
            self.send_response(head, body if not just_head else b'')

    def execute_cgi(self, path: str, method: str, body: str):
        if not os.path.exists(self.work_dir + path):
            self.send_error(404)
            return
        
        env = os.environ.copy()
        env['REQUEST_METHOD'] = method
        env['CONTENT_LENGTH'] = str(len(body))

        process = subprocess.Popen(
            ['python', f'.{path}'],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=self.work_dir,
            env=env,
        )

        stdout, stderr = process.communicate(input=body.encode('utf-8'))
        if process.returncode != 0:
            self.send_error(500)
            print(stderr.decode('utf-8'))
        else:
            head = Header(self.http_version, 200)\
                .add_header('Content-Type', 'text/html')\
                .add_header('Content-Length', str(len(stdout)))\
                .add_header('Last-Modified', date_time_string())\
                .__str__().encode('utf-8')
            self.send_response(head, stdout)

    def handle_getServerInfo(self):
        server_name = socket.gethostname()
        server_address = socket.gethostbyname(server_name)
        client_address = self.address[0]

        info = {
            "serverName": server_name,
            "serverAddress": server_address,
            "clientAddress": client_address
        }

        head = Header(self.http_version, 200)\
            .add_header('Content-Type', 'application/json')\
            .add_header('Content-Length', str(len(json.dumps(info))))\
            .add_header('Last-Modified', date_time_string())\
            .__str__().encode('utf-8')
        self.send_response(head, json.dumps(info).encode())

    def handle_GET(self, path: str):
        if path == "/getServerInfo":
            self.handle_getServerInfo()
        else:
            self.send_file(path)

    def handle_HEAD(self, path: str):
        self.send_file(path, just_head=True)

    def handle_POST(self, path: str, body: str):
        if path.startswith('/cgi-bin/'):
            self.execute_cgi(path, 'POST', body)
        else:
            self.send_error(404)

    def run(self):
        try:
            request = self.client.recv(1024).decode('utf-8')
            request_line, headers, body = parse_request(request)
            request_method, path, http_version = request_line.split()
            print(f"[{get_time()}] \"{request_line}\"")
            
            if request_method == 'GET':
                self.handle_GET(path)
            elif request_method == 'HEAD':
                self.handle_HEAD(path)
            elif request_method == 'POST':
                self.handle_POST(path, body)
            else:
                self.send_error(400)

        except Exception as e:
            print(f"Error handling client: {e}")
            self.send_error(500)
        finally:
            self.client.close()