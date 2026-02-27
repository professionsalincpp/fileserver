import hashlib
import utils.extendedmimes as extendedmimes
from typing import Dict
from fileservices.fileworkerstatus import FileWorkerStatus
from fileservices.fileworkermode import FileWorkerMode
from policyservices.policyworkermode import PolicyWorkerMode
from policyservices.policyworkerstatus import PolicyWorkerStatus
from handlers.checker import APIChecker
from fileservices.encoder import Encoder
from .response import Response
from logservices.logger import MultiLogger
from config import Config
from fileservices.fileworker import FileWorker
from policyservices.policyworker import PolicyWorker
from utils.pathutils import get_correct_path
from handlers.BaseHandler import BaseHandler


_logger = MultiLogger("posthandler")

class POSTHandler(BaseHandler):
    encodings = {
        "text/plain": "utf-8",
        "*/*": "utf-8",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": "utf-8",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document": "utf-8",
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
            return cls.wrap_error(400, "Bad Request", "Invalid request data")
        
        if path == ["read"]:
            return cls.processread(body)
        if path == ["create", "dir"]:
            return cls.processcreate_dir(body)
        if path == ["create", "file"]:
            return cls.processcreate_file(body)
        
        _logger.error("Unknown path")
        return cls.wrap_error(404, "Not Found", f"Method not found for path \"{path}\"")
    
        
    @classmethod
    def processread(cls, body: Dict[str, str]) -> Response:
        filepath = body["path"]
        filepath = get_correct_path(Config.get_config()["path"]["data"], filepath)
        body["path"] = filepath

        policyworker = PolicyWorker(Config.get_config()["path"]["data"], body, PolicyWorkerMode.CHECK_READ_PERMISSIONS)
        policyworker.run()
        msg = policyworker.get_result().data.getvalue()
        if policyworker.get_result().status != PolicyWorkerStatus.ALLOWED:
            _logger.error("Read permissions check failed")
            _logger.error(msg.decode())
            msg = cls.as_json({
                "status": "error",
                "message": "Read permissions check failed",
                "error_code": 403,
                "error_message": msg.decode()
            })
            return Response(msg, 403)
        
        fileworker = FileWorker(filepath, FileWorkerMode.READ)
        fileworker.run()
        mimetype = extendedmimes.guess_mimetype(filepath)
        if fileworker.get_result().status == FileWorkerStatus.SUCCESS:
            try:
                decoded_data = Encoder.decode(fileworker.get_result().data.getvalue(), mimetype)
            except UnicodeDecodeError as e:
                decoded_data = f"UnicodeDecodeError {e}."
                _logger.error("Unable to decode file with mimetype: " + mimetype)

            return cls.wrap_success(200, "File read successfully", {
                "data": decoded_data,
                "hash": hashlib.sha256(fileworker.get_result().data.getvalue()).hexdigest(),
                "mimetype": mimetype
            })
        if fileworker.get_result().status == FileWorkerStatus.NOT_FOUND:
            return cls.wrap_error(404, "File not found", fileworker.get_result().data.getvalue().decode())
        else:
            return cls.wrap_error(500, "Something went wrong", fileworker.get_result().data.getvalue().decode())
    
    @classmethod
    def processcreate_dir(cls, body: Dict[str, str]) -> Response:
        filepath = get_correct_path(Config.get_config()["path"]["data"], body["path"])
        print(body)
        print(filepath)
        body["path"] = filepath
        
        policyworker = PolicyWorker(Config.get_config()["path"]["data"], body, PolicyWorkerMode.CHECK_CREATE_PERMISSIONS)
        policyworker.run()
        msg = policyworker.get_result().data.getvalue()
        if policyworker.get_result().status != PolicyWorkerStatus.ALLOWED:
            return cls.wrap_error(403, "Create permissions check failed", msg.decode())
        
        fileworker = FileWorker(filepath, FileWorkerMode.CREATE_DIR)
        fileworker.run()
        if fileworker.get_result().status == FileWorkerStatus.SUCCESS:
            return cls.wrap_success(201, "Directory created successfully")
        elif fileworker.get_result().status == FileWorkerStatus.NOT_FOUND:
            return cls.wrap_error(404, "File not found", fileworker.get_result().data.getvalue().decode())
        elif fileworker.get_result().status == FileWorkerStatus.ERROR:
            return cls.wrap_error(500, "Something went wrong", fileworker.get_result().data.getvalue().decode())
    
    @classmethod
    def processcreate_file(cls, body: Dict[str, str]) -> Response:
        filepath = get_correct_path(Config.get_config()["path"]["data"], body["path"])
        body["path"] = filepath
        
        policyworker = PolicyWorker(Config.get_config()["path"]["data"], body, PolicyWorkerMode.CHECK_CREATE_PERMISSIONS)
        policyworker.run()
        if policyworker.get_result().status != PolicyWorkerStatus.ALLOWED:
            return cls.wrap_error(403, "Create permissions check failed", policyworker.get_result().data.getvalue().decode())
        
        fileworker = FileWorker(filepath, FileWorkerMode.CREATE_FILE)
        fileworker.run()
        if fileworker.get_result().status == FileWorkerStatus.SUCCESS:
            return cls.wrap_success(201, "File created successfully")
        elif fileworker.get_result().status == FileWorkerStatus.ALREADY_EXISTS:
            return cls.wrap_error(409, "File already exists", fileworker.get_result().data.getvalue().decode())
        else:
            return cls.wrap_error(500, "Something went wrong", fileworker.get_result().data.getvalue().decode())