from .handler import RequestHandler
import socket

__all__ = ['HTTPServer']

class HTTPServer:
    def __init__(self, 
            host: str, port: int, max_conn: int, timeout: int, 
            work_dir: str, http_version: str
        ):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((host, port))
        self.server.listen(max_conn)
        self.server.settimeout(timeout)
        self.work_dir = work_dir
        self.version = http_version
        hostname = socket.gethostname()
        print(f"{hostname}: http://{socket.gethostbyname(hostname)}:{port}/")

    def run(self):
        try:
            while True:
                client, addr = self.server.accept()
                print(f'Accepted connection from {addr}')
                RequestHandler(
                    client = client, 
                    address = addr,
                    work_dir = self.work_dir,
                    http_version = self.version,
                    daemon = True
                ).start()

        except KeyboardInterrupt:
            self.server.close()
            print("\nServer stopped.")
