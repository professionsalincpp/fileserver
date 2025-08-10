from io import BytesIO
from typing import List, Literal
from .providerstatus import ProviderStatus


class ProviderResult:
    def __init__(self, data: List[str] = None, status: ProviderStatus = None, type: Literal['file', 'directory'] = None):
        self.data: List[str] = data
        self.status: ProviderStatus = status
        self.type: Literal['file', 'directory'] = type