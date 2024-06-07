from .status import get_status_str

class Header:
    def __init__(self, version: str, status_code: int):
        self.version = version
        self.status_code = status_code
        self.headers = {}

    def add_header(self, key: str, value: str):
        self.headers[key] = value
        return self

    def __str__(self):
        type = f"{self.version} {get_status_str(self.status_code)}\r\n"
        headers = '\r\n'.join([f"{k}: {v}" for k, v in self.headers.items()])
        return type + headers + '\r\n\r\n'