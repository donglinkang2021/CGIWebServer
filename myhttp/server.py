from .handler import RequestHandler
import socket
import threading
import queue

__all__ = ['HTTPServer']

class HTTPServer:
    def __init__(self, 
            host: str, port: int, max_conn: int, timeout: int, 
            work_dir: str, http_version: str
        ):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((host, port))
        server.listen(max_conn)
        server.settimeout(timeout)

        self.server_socket = server
        self.work_dir = work_dir
        self.version = http_version
        hostname = socket.gethostname()
        print(f"{hostname}: http://{socket.gethostbyname(hostname)}:{port}/")

        self.connections = queue.Queue() # to manage the thread pool
        self.max_conn = max_conn

    def run(self):
        try:
            while True:
                try:
                    self.server_socket.settimeout(0.1)
                    client_socket, client_address = self.server_socket.accept()
                except socket.timeout:
                    continue
                
                with threading.Lock():
                    if self.connections.qsize() >= self.max_conn:
                        oldest_socket, oldest_address = self.connections.get()
                        print(f"Max connections reached. Closing oldest connection from {oldest_address}")
                        oldest_socket.close()

                    self.connections.put((client_socket, client_address))
                    print(f'Accepted connection from {client_address}')
                
                    RequestHandler(
                        client = client_socket, 
                        address = client_address,
                        work_dir = self.work_dir,
                        http_version = self.version,
                        daemon = True
                    ).start()

        except KeyboardInterrupt:
            print("Server is shutting down due to KeyboardInterrupt")
        except Exception as e:
            print(f"Server error: {e}")
        finally:
            self.server_socket.close()
            while not self.connections.empty():
                sock, addr = self.connections.get()
                sock.close()
            print("Server shutdown complete")
