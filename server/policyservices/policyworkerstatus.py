from enum import Enum


class PolicyWorkerStatus(Enum):
    ALLOWED = 0,
    NOT_IN_ALLOWED_DIR = 1,
    IN_DENIED_DIR = 2,
    ERROR = 3
