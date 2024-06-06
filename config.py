# socket
MAX_CONN = 10 # MAX_CONNECTIONS
HOST, PORT = '0.0.0.0', 8888
ADDR = (HOST, PORT)
TIMEOUT = 60

# webroot
DOCUMENT_ROOT = './webroot'  # Web文档的根目录

# http
HTTP_RESPONSES = {
    200: "OK",
    400: "Bad Request",
    403: "Forbidden",
    404: "Not Found"
}