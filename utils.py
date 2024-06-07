import time
from email.utils import formatdate
from typing import Tuple

__all__ = [
    'get_time', 
    'addr2str',
    'date_time_string'
]

def get_time(timefmt:str='%Y-%m-%d_%H-%M-%S') -> str:
    return time.strftime(timefmt, time.localtime(time.time()))

def addr2str(addr:Tuple[str, int]) -> str:
    return f"{addr[0]}:{addr[1]}"

def date_time_string():
    return formatdate(time.time(), usegmt=True)