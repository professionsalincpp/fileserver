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

_logger = MultiLogger("deletehandler")

class DELETEHandler(BaseHandler):
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
            _logger.error("Request body is not valid", context="deletehandler")
            return cls.wrap_error(400, "Bad Request", "Invalid request data")

        if path == ["delete"]:
            return cls.processdelete(body)
        
        _logger.error("Unknown path", context="deletehandler")
        return cls.wrap_error(404, "Not Found", f"Method not found for path \"{path}\"")
    
    @classmethod
    def processdelete(cls, body: Dict[str, str]) -> Response:
        path = body["path"]
        path = get_correct_path(Config.get_config()["path"]["data"], path)
        body["path"] = path

        policyworker = PolicyWorker(Config.get_config()["path"]["data"], body, PolicyWorkerMode.CHECK_DELETE_PERMISSIONS)
        policyworker.run()
        msg = policyworker.get_result().data.getvalue()
        if policyworker.get_result().status != PolicyWorkerStatus.ALLOWED:
            _logger.error("Delete permissions check failed", context="deletehandler")
            _logger.error(msg.decode())
            return cls.wrap_error(403, "Forbidden", msg.decode())
        
        fileworker = FileWorker(path, FileWorkerMode.DELETE)
        fileworker.run()
        if fileworker.get_result().status == FileWorkerStatus.SUCCESS:
            return cls.wrap_success(200, "File deleted successfully")
        if fileworker.get_result().status == FileWorkerStatus.NOT_FOUND:
            return cls.wrap_error(404, "File not found", fileworker.get_result().data.getvalue().decode())
        else:
            return cls.wrap_error(500, "Something went wrong", fileworker.get_result().data.getvalue().decode())