import pathlib
from utils.path import get_correct_path
from .policyworkerresult import PolicyWorkerResult
from .policyworkermode import PolicyWorkerMode
from .policyworkerstatus import PolicyWorkerStatus


class PolicyWorker:
    def __init__(self, data_dir: str, data: dict, mode: PolicyWorkerMode) -> None:
        self.data_dir = pathlib.Path(data_dir).resolve()
        self.mode = mode
        self.data = data
        self.result = PolicyWorkerResult()

    def is_path_inside(self, path: str):
        abs_path = pathlib.Path(path).resolve()
        return str(self.data_dir) in str(abs_path)
    
    def check_mode(self) -> bool:
        return self.mode in PolicyWorkerMode    
    
    def run(self) -> None:
        if not self.check_mode():
            self.result.status = PolicyWorkerStatus.ERROR
            self.result.data.write(f"Invalid mode {self.mode=}".encode())
            return
        
        method = f"_{self.mode.name.lower()}"
        getattr(self, method)()

    def _check_write_permissions(self):
        try:
            _path = self.data["path"]
            if not self.is_path_inside(_path):
                self.result.status = PolicyWorkerStatus.NOT_IN_ALLOWED_DIR
                self.result.data.write(f"Not in allowed dir {_path}".encode())
                return
            self.result.status = PolicyWorkerStatus.ALLOWED
        except Exception as e:
            self.write_error(e)

    def _check_read_permissions(self):
        try:
            _path = self.data["path"]
            if not self.is_path_inside(_path):
                self.result.status = PolicyWorkerStatus.NOT_IN_ALLOWED_DIR
                self.result.data.write(f"Not in allowed dir {_path}".encode())
                return
            self.result.status = PolicyWorkerStatus.ALLOWED
        except Exception as e:
            self.write_error(e)

    def _check_copy_permissions(self):
        try:
            _src_path = self.data["path"]["source"]
            _dst_path = self.data["path"]["dest"]
            if not self.is_path_inside(_dst_path):
                self.result.status = PolicyWorkerStatus.NOT_IN_ALLOWED_DIR
                self.result.data.write(f"Not in allowed dir {_src_path}".encode())
                return
            if not self.is_path_inside(_src_path):
                self.result.status = PolicyWorkerStatus.NOT_IN_ALLOWED_DIR
                self.result.data.write(f"Not in allowed dir {_dst_path}".encode())
                return
            self.result.status = PolicyWorkerStatus.ALLOWED
        except Exception as e:
            self.write_error(e)
    
    def _check_move_permissions(self):
        try:
            _src_path = self.data["path"]["source"]
            _dst_path = self.data["path"]["dest"]
            if not self.is_path_inside(_dst_path):
                self.result.status = PolicyWorkerStatus.NOT_IN_ALLOWED_DIR
                self.result.data.write(f"Not in allowed dir {_src_path}".encode())
                return
            if not self.is_path_inside(_src_path):
                self.result.status = PolicyWorkerStatus.NOT_IN_ALLOWED_DIR
                self.result.data.write(f"Not in allowed dir {_dst_path}".encode())
                return
            self.result.status = PolicyWorkerStatus.ALLOWED
        except Exception as e:
            self.write_error(e)

    def _check_create_permissions(self):
        try:
            _path = self.data["path"]
            if not self.is_path_inside(_path):
                self.result.status = PolicyWorkerStatus.NOT_IN_ALLOWED_DIR
                self.result.data.write(f"Not in allowed dir {_path}".encode())
                return
            self.result.status = PolicyWorkerStatus.ALLOWED
        except Exception as e:
            self.write_error(e)

    def write_error(self, exception: Exception) -> None:
        self.result.status = PolicyWorkerStatus.ERROR
        self.result.data.write("PolicyWorker: ".encode() + str(exception).encode())
        
    def get_result(self) -> PolicyWorkerResult:
        return self.result
    
