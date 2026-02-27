import os
import shutil
from .fileworkerresult import FileWorkerResult
from .fileworkermode import FileWorkerMode
from .fileworkerstatus import FileWorkerStatus
from logservices.logger import MultiLogger
from typing import Optional

_logger = MultiLogger("fileworker")

class FileWorker:
    def __init__(self, path: str, mode: FileWorkerMode, data: Optional[bytes]=None):
        self.mode = mode
        self.path = path
        self.data = data
        self.result: FileWorkerResult = FileWorkerResult()

    def run(self) -> None:
        if not self.check_path():
            _logger.error(f"Path \"{self.path}\" not found", context="fileworker")
            self.result.status = FileWorkerStatus.NOT_FOUND
            self.result.data.write(f"Path \"{self.path}\" not found".encode())
            return
        if not self.check_mode():
            _logger.error(f"Invalid mode {self.mode=}")
            self.result.status = FileWorkerStatus.ERROR
            self.result.data.write(f"Invalid mode {self.mode=}".encode())
            return
        
        method = f"_run_{self.mode.name.lower()}"
        getattr(self, method)()

    def get_result(self) -> FileWorkerResult:
        return self.result
    
    def _run_read(self):
        try:
            with open(self.path, 'rb') as file:
                self.result.data.write(file.read())
            self.result.status = FileWorkerStatus.SUCCESS
        except Exception as e:
            self.write_error(e)

    def _run_rename(self):
        try:
            os.rename(self.path["old"], self.path["new"])
            self.result.status = FileWorkerStatus.SUCCESS
        except Exception as e:
            _logger.error(f"Raised exception {self.path=} {self.data=} {e=}")
            self.write_error(e)

    def _run_write(self):
        try:
            with open(self.path, 'wb') as file:
                file.write(self.data)
            self.result.status = FileWorkerStatus.SUCCESS
        except Exception as e:
            _logger.error(f"Raised exception {self.path=} {self.data=} {e=}")
            self.write_error(e)
    
    def _run_copy(self):
        try:
            if os.path.isdir(self.path["source"]):
                _logger.info(f"Copying directory {self.path['source']} to {self.path['dest']}")
                shutil.copytree(self.path["source"], self.path["dest"])
                self.result.status = FileWorkerStatus.SUCCESS
                return
            shutil.copyfile(self.path["source"], self.path["dest"])
            self.result.status = FileWorkerStatus.SUCCESS
        except Exception as e:
            _logger.error(f"Raised exception {self.path=} {self.data=} {e=}")
            self.write_error(e)
    
    def _run_move(self):
        try:
            shutil.move(self.path["source"], self.path["dest"])
            if os.path.exists(self.path["source"]):
                os.remove(self.path["source"])
            self.result.status = FileWorkerStatus.SUCCESS

        except Exception as e:
            _logger.error(f"Raised exception {self.path=} {self.data=} {e=}")
            self.write_error(e)
    
    def _run_create_dir(self):
        try:
            os.makedirs(self.path)
            self.result.status = FileWorkerStatus.SUCCESS
        except Exception as e:
            _logger.error(f"Raised exception {self.path=} {self.data=} {e=}")
            self.write_error(e)

    def _run_create_file(self):
        try:
            with open(self.path, 'w') as file:
                file.write("")
            self.result.status = FileWorkerStatus.SUCCESS
        except Exception as e:
            _logger.error(f"Raised exception {self.path=} {self.data=} {e=}")
            self.write_error(e)

    def _run_delete(self):
        try:
            if os.path.isdir(self.path):
                shutil.rmtree(self.path)
            else:
                os.remove(self.path)
            self.result.status = FileWorkerStatus.SUCCESS
        except Exception as e:
            _logger.error(f"Raised exception {self.path=} {self.data=} {e=}")
            self.write_error(e)

    def write_error(self, exception: Exception) -> None:
        self.result.status = FileWorkerStatus.ERROR
        self.result.data.write(str(exception).encode())

    def check_path(self) -> bool:
        if self.mode in (FileWorkerMode.COPY, FileWorkerMode.MOVE):
            if not os.path.exists(self.path["source"]):
                _logger.error(f"Source file not found {self.path=}")
                self.result.status = FileWorkerStatus.NOT_FOUND
                self.result.data.write(f"Source file not found {self.path=}".encode())
                return False
            return True
        if self.mode in (FileWorkerMode.RENAME,):
            if not os.path.exists(self.path["old"]):
                _logger.error(f"Source file not found {self.path=}")
                self.result.status = FileWorkerStatus.NOT_FOUND
                self.result.data.write(f"Source file not found {self.path=}".encode())
                return False
            return True
        if self.mode in (FileWorkerMode.WRITE, FileWorkerMode.CREATE_DIR, FileWorkerMode.CREATE_FILE) or os.path.exists(self.path):
            return True
        return False
    
    def check_mode(self) -> bool:
        if self.mode in FileWorkerMode:
            return True
        return False