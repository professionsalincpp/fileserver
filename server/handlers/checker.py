import hashlib
from typing import List, Dict
from logservices.logger import MultiLogger
from api import basic_structure

_logger = MultiLogger("postchecker")



class APIChecker:
    @classmethod
    def check_is_api(cls, path: List[str]) -> bool:
        if path[0] == "api":
            return True
        else:
            return False
        
    @classmethod
    def check_data_integrity(cls, data: bytes, hash: str) -> bool:
        
        actual_hash = hashlib.sha256(data).hexdigest()
        if actual_hash == hash:
            return True
        _logger.error(f"Integrity check failed, actual hash: {hash}, expected hash: {actual_hash}")
        return False
    
    @classmethod
    def check_request_body_is_valid(cls, body: Dict[str, str], path: str) -> bool:
        strpath: str = '/'.join(path)
        return basic_structure.validate(strpath, body)