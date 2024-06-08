import os
import subprocess
import threading
import socket
import json
from .header import Header
from .status import get_status_str
from .utils import *
import urllib.parse

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
        cur_path = self.work_dir + path
        cur_path = urllib.parse.unquote(cur_path)
        if os.path.isdir(cur_path):
            if not path.endswith('/'):
                self.send_response(Header(self.http_version, 301)\
                    .add_header('Location', path + '/')\
                    .add_header('Content-Length', '0')\
                    .__str__().encode('utf-8'))
                return
            for index in ["index.html", "index.htm"]:
                index = os.path.join(cur_path, index)
                if os.path.isfile(index):
                    print(f"Index file found: {index}")
                    cur_path = index
                    break
            else:
                self.list_directory(cur_path)
                return
    
        try:
            f = open(cur_path, 'rb')
            body = f.read()
            f.close()
        except OSError:
            self.send_error(404)
            return
        
        head = Header(self.http_version, 200)\
            .add_header('Content-Type', get_content_type(cur_path))\
            .add_header('Content-Length', str(len(body)))\
            .add_header('Last-Modified', date_time_string())\
            .__str__().encode('utf-8')
        
        if just_head:
            self.send_response(head)
        else:
            self.send_response(head, body)

    def list_directory(self, path: str):
        try:
            list = os.listdir(path)
        except OSError:
            self.send_error(404)
            return
        list.sort(key=lambda a: a.lower())
        r = []
        displaypath = path
        enc = 'utf-8'
        title = f'Directory listing for {displaypath}'
        r.append('<!DOCTYPE HTML>')
        r.append('<html lang="en">')
        r.append('<head>')
        r.append(f'<meta charset="{enc}">')
        r.append(f'<title>{title}</title>\n</head>')
        r.append(f'<body>\n<h1>{title}</h1>')
        r.append('<hr>\n<ul>')
        for name in list:
            fullname = os.path.join(path, name)
            displayname = linkname = name
            if os.path.isdir(fullname):
                displayname = name + "/"
                linkname = name + "/"
            if os.path.islink(fullname):
                displayname = name + "@"
            r.append('<li><a href="%s">%s</a></li>'
                    % (linkname, displayname))
        r.append('</ul>\n<hr>\n</body>\n</html>\n')
        body = '\n'.join(r).encode(enc)
        head = Header(self.http_version, 200)\
            .add_header('Content-Type', 'text/html')\
            .add_header('Content-Length', str(len(body)))\
            .add_header('Last-Modified', date_time_string())\
            .__str__().encode('utf-8')
        self.send_response(head, body)

    def execute_cgi(self, path: str, method: str, body: str, headers: dict):
        if not os.path.exists(self.work_dir + path):
            self.send_error(404)
            return
        
        env = os.environ.copy()
        env['REQUEST_METHOD'] = method
        env['CONTENT_LENGTH'] = str(len(body))
        env['CONTENT_TYPE'] = headers.get('Content-Type', 'text/plain')
        
        process = subprocess.Popen(
            ['python', '-u', f'.{path}'],
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
            out = stdout.decode('utf-8')
            content_type, content = out.split('\r\n\r\n', 1)
            content = content.encode('utf-8')
            content_type = content_type.split(': ')[1]
            head = Header(self.http_version, 200)\
                .add_header('Content-Type', content_type)\
                .add_header('Content-Length', str(len(content)))\
                .add_header('Last-Modified', date_time_string())\
                .__str__().encode('utf-8')
            self.send_response(head + content)

    def handle_GET(self, path: str):
        self.send_file(path)

    def handle_HEAD(self, path: str):
        self.send_file(path, just_head=True)

    def handle_POST(self, path: str, body: str, headers: dict):
        if path.startswith('/cgi-bin/'):
            self.execute_cgi(path, 'POST', body, headers)
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
                self.handle_POST(path, body, headers)
            else:
                self.send_error(400)

        except Exception as e:
            print(f"Error handling client: {e}")
        finally:
            print(f"Connection from {self.address} closed")
            self.client.close()