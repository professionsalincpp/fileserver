from io import BytesIO
from .fileworkerstatus import FileWorkerStatus


class FileWorkerResult:
    def __init__(self):
        self.data: BytesIO = BytesIO()
        self.status: FileWorkerStatus = None