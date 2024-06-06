from config import *

def handle_client(client_socket:socket.socket):
    try:
        request = client_socket.recv(1024).decode('utf-8')
        print("-" * 40)
        print(f"Received request: {request}")
        print("-" * 40)
        if not request:
            return

        # 解析HTTP请求
        headers = request.split('\r\n')
        method, path, _ = headers[0].split()
        path = urllib.parse.unquote(path)

        if method not in ["GET", "POST", "HEAD"]:
            send_response(client_socket, 400)
            return

        if '..' in path or path.startswith('/'):
            send_response(client_socket, 403)
            return

        if method == "POST":
            body = request.split('\r\n\r\n', 1)[1]
        else:
            body = None

        handle_request(client_socket, method, path, body)
    except Exception as e:
        print(f"Client handling error: {e}")
    finally:
        client_socket.close()
        with connection_lock:
            client_threads.remove(threading.current_thread())
        print("Connection closed")

def handle_request(client_socket:socket.socket, method, path, body):
    if path == '/':
        path = '/index.html'
    file_path = DOCUMENT_ROOT + path

    if os.path.isdir(file_path):
        file_path += '/index.html'

    if not os.path.exists(file_path):
        send_response(client_socket, 404)
        return

    if not os.access(file_path, os.R_OK):
        send_response(client_socket, 403)
        return

    if file_path.endswith('.cgi'):
        execute_cgi(client_socket, file_path, body)
    else:
        send_file(client_socket, file_path, method)

def execute_cgi(client_socket, file_path, body):
    env = os.environ.copy()
    env['REQUEST_METHOD'] = 'POST' if body else 'GET'
    if body:
        env['CONTENT_LENGTH'] = str(len(body))
    
    process = os.popen(file_path)
    output = process.read()
    process.close()

    response = f"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n{output}"
    client_socket.sendall(response.encode('utf-8'))

def send_file(client_socket, file_path, method):
    with open(file_path, 'rb') as f:
        content = f.read()

    if method != "HEAD":
        response = f"HTTP/1.1 200 OK\r\nContent-Length: {len(content)}\r\n\r\n".encode('utf-8') + content
    else:
        response = f"HTTP/1.1 200 OK\r\nContent-Length: {len(content)}\r\n\r\n".encode('utf-8')

    client_socket.sendall(response)

def send_response(client_socket, status_code):
    response = f"HTTP/1.1 {status_code} {HTTP_RESPONSES[status_code]}\r\n\r\n{HTTP_RESPONSES[status_code]}"
    client_socket.sendall(response.encode('utf-8'))

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    address = ('127.0.0.1', PORT)
    server_socket.bind(address)
    server_socket.listen()
    print(f"Server listening on port {PORT}")
    print(f"Document root is {DOCUMENT_ROOT}")
    print(f"Max connections: {MAX_CONNECTIONS}")
    print("You can access the server through http://" + address[0] + ":" + str(address[1]))
    print("Press Ctrl+C to stop the server")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Accepted connection from {addr}")

        with connection_lock:
            if len(client_threads) >= MAX_CONNECTIONS:
                oldest_thread = client_threads.pop(0)
                oldest_thread.client_socket.close()
                oldest_thread.join()

            client_thread = threading.Thread(target=handle_client, args=(client_socket,))
            client_thread.client_socket = client_socket  # 存储socket在线程对象中
            client_threads.append(client_thread)
            client_thread.start()

        

    server_socket.close()

if __name__ == "__main__":
    connection_lock = threading.Lock()
    client_threads = []
    main()
