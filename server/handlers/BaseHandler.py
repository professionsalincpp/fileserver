import json
from typing import Dict, Optional
from handlers.response import Response

class BaseHandler:
    SERVER_URL: str = ...
    @classmethod
    def wrap_error(cls, status_code: int, message: str, error_message: str) -> Response:
        return Response(cls.as_json({"status": "error", "message": message, "error_code": status_code, "error_message": error_message}), status_code)
    
    @classmethod
    def wrap_success(cls, status_code: int, message: str, data: Optional[Dict[str, str]]=None) -> Response:
        if data:
            return Response(cls.as_json({"status": "success", "message": message, "data": data}), status_code)
        return Response(cls.as_json({"status": "success", "message": message}), status_code)
    
    @classmethod
    def as_json(cls, data: Dict[str, str]) -> bytes:
        return json.dumps(data).encode()
        