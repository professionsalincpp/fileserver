from enum import Enum

class FileWorkerMode(Enum):
    """
    Enum for file worker mode
    """
    READ = 0
    WRITE = 1
    COPY = 2
    MOVE = 3
    CREATE_DIR = 4
    CREATE_FILE = 5,
    LIST_DIR = 6,
    DELETE = 7,
    RENAME = 8
