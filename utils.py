import time
from typing import Tuple

__all__ = [
    'get_time', 
    'addr2str',
]

def get_time(timefmt:str='%Y-%m-%d_%H-%M-%S') -> str:
    return time.strftime(timefmt, time.localtime(time.time()))

def addr2str(addr:Tuple[str, int]) -> str:
    return f"{addr[0]}:{addr[1]}"