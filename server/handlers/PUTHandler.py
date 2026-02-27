import hashlib
import mimetypes
from typing import Dict
from fileservices.fileworkerstatus import FileWorkerStatus
from fileservices.fileworkermode import FileWorkerMode
from policyservices.policyworkermode import PolicyWorkerMode
from policyservices.policyworkerstatus import PolicyWorkerStatus
from handlers.checker import APIChecker
import utils.extendedmimes as extendedmimes
from .response import Response
from logservices.logger import MultiLogger
from config import Config
from fileservices.fileworker import FileWorker
from policyservices.policyworker import PolicyWorker
from utils.pathutils import get_correct_path
from handlers.BaseHandler import BaseHandler
from fileservices.encoder import Encoder

_logger = MultiLogger("puthandler")

class PUTHandler(BaseHandler):
    encodings = {
        "text/plain": "utf-8",
        "*/*": "utf-8",
        "image/bmp": "latin1",
        "image/png": "latin1",
        "image/jpeg": "latin1",
        "image/gif": "latin1",
        "image/pdf": "latin1"
    }
    @classmethod
    def processrequest(cls, body: Dict[str, str], path: str) -> Response:
        if not APIChecker.check_is_api(path):
            return cls.wrap_error(404, "Not Found", "Not an API request")
        else:
            path = path[1:]
        if not APIChecker.check_request_body_is_valid(body, path): 
            _logger.error("Request body is not valid", context="puthandler")
            return cls.wrap_error(400, "Bad Request", "Invalid request data")

        if path == ["copy"]:
            return cls.processcopy(body)
        if path == ["move"]:
            return cls.processmove(body)
        if path == ["write"]:
            return cls.processwrite(body)
        if path == ["rename"]:
            return cls.processrename(body)        
        
        _logger.error("Unknown path", context="puthandler")
        return cls.wrap_error(404, "Not Found", f"Method not found for path \"{path}\"")
    

    @classmethod
    def processrename(cls, body: Dict[str, str]) -> Response:
        file_path_old: str = body["path"]["old"]
        if file_path_old == body["path"]["new"]:
            if file_path_old == "/":
                return cls.wrap_error(400, "Bad Request", "Cannot rename root directory")
            else:
                return cls.wrap_error(400, "Bad Request", "Cannot rename to the same path")
        file_path_new: str = body["path"]["new"]
        file_path_old = get_correct_path(Config.get_config()["path"]["data"], file_path_old)
        file_path_new = get_correct_path(Config.get_config()["path"]["data"], file_path_new)
        body["path"]["old"] = file_path_old
        body["path"]["new"] = file_path_new
        
        policyworker = PolicyWorker(Config.get_config()["path"]["data"], body, PolicyWorkerMode.CHECK_RENAME_PERMISSIONS)
        policyworker.run()
        msg = policyworker.get_result().data.getvalue()
        if policyworker.get_result().status != PolicyWorkerStatus.ALLOWED:
            return cls.wrap_error(403, "Forbidden", msg.decode())

        fileworker = FileWorker({"old": file_path_old, "new": file_path_new}, FileWorkerMode.RENAME)
        fileworker.run()
        if fileworker.get_result().status == FileWorkerStatus.SUCCESS:
            return cls.wrap_success(200, "File renamed successfully")
        if fileworker.get_result().status == FileWorkerStatus.NOT_FOUND:
            return cls.wrap_error(404, "File not found", fileworker.get_result().data.getvalue().decode())
        else:
            return cls.wrap_error(500, "Something went wrong", fileworker.get_result().data.getvalue().decode())
    
    @classmethod
    def processwrite(cls, body: Dict[str, str]) -> Response:
        filepath = body["path"]
        data: str = body["data"]
        data_hash: str = body["hash"]
        mimetype = extendedmimes.guess_mimetype(filepath)
        actual_data = Encoder.encode(data, mimetype)
        # bytes_data = actual_data.encode("utf-8")
        if not APIChecker.check_data_integrity(data.encode("utf-8"), data_hash):
            _logger.error("Data integrity check failed")
            return cls.wrap_error(400, "Bad Request", "Data integrity check failed")
            
        full_file_path : str = get_correct_path(Config.get_config()["path"]["data"], filepath)  
        body["path"] = full_file_path  

        policyworker = PolicyWorker(Config.get_config()["path"]["data"], body, PolicyWorkerMode.CHECK_WRITE_PERMISSIONS)
        policyworker.run()
        msg = policyworker.get_result().data.getvalue()

        if policyworker.get_result().status != PolicyWorkerStatus.ALLOWED:
            _logger.error("Write permissions check failed")
            _logger.error(msg.decode())
            return cls.wrap_error(403, "Forbidden", msg.decode())
        
        fileworker = FileWorker(full_file_path, FileWorkerMode.WRITE, actual_data)
        fileworker.run()
        if fileworker.get_result().status == FileWorkerStatus.SUCCESS:
            return cls.wrap_success(200, "File written successfully")
        if fileworker.get_result().status == FileWorkerStatus.NOT_FOUND:
            return cls.wrap_error(404, "File not found", fileworker.get_result().data.getvalue().decode())
        else:
            return cls.wrap_error(500, "Something went wrong", fileworker.get_result().data.getvalue().decode())
        
        
    @classmethod
    def processcopy(cls, body: Dict[str, str]) -> Response:
        paths = body["path"]
        paths["source"] = get_correct_path(Config.get_config()["path"]["data"], paths["source"])
        paths["dest"] = get_correct_path(Config.get_config()["path"]["data"], paths["dest"])

        policyworker = PolicyWorker(Config.get_config()["path"]["data"], body, PolicyWorkerMode.CHECK_COPY_PERMISSIONS)
        policyworker.run()
        msg = policyworker.get_result().data.getvalue()
        if policyworker.get_result().status != PolicyWorkerStatus.ALLOWED:
            return Response(msg, 403)
        
        fileworker = FileWorker(paths, FileWorkerMode.COPY)
        fileworker.run()
        if fileworker.get_result().status == FileWorkerStatus.SUCCESS:
            return cls.wrap_success(201, "File copied successfully")
        if fileworker.get_result().status == FileWorkerStatus.NOT_FOUND:
            return cls.wrap_error(404, "File not found", fileworker.get_result().data.getvalue().decode())
        else:
            return cls.wrap_error(500, "Something went wrong", fileworker.get_result().data.getvalue().decode())
    
    @classmethod
    def processmove(cls, body: Dict[str, str]) -> Response:
        paths = body["path"]
        paths["source"] = get_correct_path(Config.get_config()["path"]["data"], paths["source"])
        paths["dest"] = get_correct_path(Config.get_config()["path"]["data"], paths["dest"])

        policyworker = PolicyWorker(Config.get_config()["path"]["data"], body, PolicyWorkerMode.CHECK_MOVE_PERMISSIONS)
        policyworker.run()
        msg = policyworker.get_result().data.getvalue()
        if policyworker.get_result().status != PolicyWorkerStatus.ALLOWED:
            return cls.wrap_error(403, "Forbidden", msg.decode())
        
        fileworker = FileWorker(paths, FileWorkerMode.MOVE)
        fileworker.run()
        if fileworker.get_result().status == FileWorkerStatus.SUCCESS:
            return cls.wrap_success(200, "File moved successfully")
        if fileworker.get_result().status == FileWorkerStatus.NOT_FOUND:
            return cls.wrap_error(404, "File not found", fileworker.get_result().data.getvalue().decode())
        else:

            return cls.wrap_error(500, "Something went wrong", fileworker.get_result().data.getvalue().decode())