"""
Response class for the handlers
"""
from typing import Dict

class Response:
    def __init__(self, body: bytes, status_code: int, headers: Dict[str, str] = {}) -> None:
        self.status_code: int = status_code
        self.headers: Dict[str, str] = headers
        self.body: bytes = body

