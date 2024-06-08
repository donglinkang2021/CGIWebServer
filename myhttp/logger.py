import logging
from .utils import date_time_string, addr2str, get_time
from typing import Tuple
from pathlib import Path

class Logger:
    def __init__(self, work_dir:str):
        log_dir = Path(work_dir) / 'log'
        log_dir.mkdir(exist_ok=True)
        log_file = log_dir / f'{get_time()}.txt'
        logging.basicConfig(
            level=logging.INFO,
            format='%(message)s',
            datefmt='%Y-%m-%d %H:%M:%S',
            filename=log_file,
            filemode='w'
        )
        self.reset()

    def reset(self):
        self.remote_addr = None
        self.request_time = None
        self.request_line = None
        self.request_user_agent = None
        self.request_referer = None

        self.response_status = None
        self.response_content_length = None

    def log_request(
            self,
            address:str,
            request_line:str,
            headers:dict,
        ) -> None:
        self.remote_addr = address
        self.request_time = date_time_string(localtime=True)
        self.request_line = request_line
        self.request_user_agent = headers.get('User-Agent', '')
        self.request_referer = headers.get('Referer', '')

    def log_response(
            self,
            status:int, 
            content_length:int = 0
        ) -> None:
        self.response_status = status
        self.response_content_length = content_length

    def log(self):
        logging.info(
            f"{self.remote_addr} -- [{self.request_time}]"
            f' "{self.request_line}"'
            f' {self.response_status}'
            f' {self.response_content_length}'
            f' "{self.request_referer}"'
            f' "{self.request_user_agent}"'
        )
        self.reset()

    

    