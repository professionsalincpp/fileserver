from enum import Enum


class FileWorkerStatus(Enum):
    SUCCESS = 1
    ERROR = 2
    NOT_FOUND = 3
    ALREADY_EXISTS = 4
    