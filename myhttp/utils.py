import time
from email.utils import formatdate
from typing import Tuple

__all__ = [
    'parse_request',
    'get_time', 
    'addr2str',
    'date_time_string',
    'get_content_type'
]

def parse_request(request: str) -> Tuple[str, dict, str]:
    head, body = request.split('\r\n\r\n', 1)
    request_line = head.splitlines()[0]
    headers = dict([line.split(': ', 1) for line in head.splitlines()[1:]])
    return request_line, headers, body

def get_time(timefmt:str='%Y-%m-%d_%H-%M-%S') -> str:
    return time.strftime(timefmt, time.localtime(time.time()))

def addr2str(addr:Tuple[str, int]) -> str:
    return f"{addr[0]}:{addr[1]}"

def date_time_string():
    return formatdate(time.time(), usegmt=True)

def get_content_type(file_path:str) -> str:
    if file_path.endswith('.html'):
        return 'text/html'
    elif file_path.endswith('.css'):
        return 'text/css'
    elif file_path.endswith('.js'):
        return 'application/javascript'
    elif file_path.endswith('.png'):
        return 'image/png'
    elif file_path.endswith('.jpg') or file_path.endswith('.jpeg'):
        return 'image/jpeg'
    elif file_path.endswith('.gif'):
        return 'image/gif'
    elif file_path.endswith('.svg'):
        return 'image/svg+xml'
    else:
        return 'application/octet-stream'