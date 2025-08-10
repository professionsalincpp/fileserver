from enum import Enum


class ProviderStatus(Enum):
    SUCCESS = 1
    ERROR = 2
    NOT_FOUND = 3