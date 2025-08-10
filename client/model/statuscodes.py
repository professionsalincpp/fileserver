"""
Status codes for the commands.
When a command is executed, the command will return response with a status code.

Writen by: professionsalincpp on 07.07.2025
"""

class CommandStatusCode:
    CODE = type("CommandStatusCode", (), {})
    # Server codes
    SERVER_OK = 200
    SERVER_CREATED = 201
    SERVER_BAD_REQUEST = 400
    SERVER_FILE_NOT_FOUND = 404
    SERVER_INTERNAL_ERROR = 500
    # Client codes
    CLIENT_OK = 1200
    CLIENT_INVALID_DATA = 1400
    CLIENT_FILE_NOT_FOUND = 1401

    STRING_REPRESENTATION = {
        SERVER_OK: "SERVER_OK",
        SERVER_CREATED: "SERVER_CREATED",
        SERVER_BAD_REQUEST: "SERVER_BAD_REQUEST",
        SERVER_FILE_NOT_FOUND: "SERVER_FILE_NOT_FOUND",
        SERVER_INTERNAL_ERROR: "SERVER_INTERNAL_ERROR",
        CLIENT_OK: "CLIENT_OK",
        CLIENT_INVALID_DATA: "CLIENT_INVALID_DATA",
        CLIENT_FILE_NOT_FOUND: "CLIENT_FILE_NOT_FOUND"
    }

    INT_REPRESENTATION = {
        "SERVER_OK": SERVER_OK,
        "SERVER_CREATED": SERVER_CREATED,
        "SERVER_BAD_REQUEST": SERVER_BAD_REQUEST,
        "SERVER_FILE_NOT_FOUND": SERVER_FILE_NOT_FOUND,
        "SERVER_INTERNAL_ERROR": SERVER_INTERNAL_ERROR,
        "CLIENT_OK": CLIENT_OK,
        "CLIENT_INVALID_DATA": CLIENT_INVALID_DATA,
        "CLIENT_FILE_NOT_FOUND": CLIENT_FILE_NOT_FOUND
    }

    @staticmethod
    def to_string(code: int) -> str:
        return CommandStatusCode.STRING_REPRESENTATION.get(code, "UNKNOWN_ERROR")
    
    @staticmethod
    def to_int(code: str) -> int:
        return CommandStatusCode.INT_REPRESENTATION.get(code, CommandStatusCode.SERVER_INTERNAL_ERROR)
    
    @staticmethod
    def is_server_code(code: int) -> bool:
        if code >= 200 and code <= 500:
            return True
        else:
            return False

    @staticmethod
    def is_client_code(code: int) -> bool:
        if code >= 1200 and code < 1400:
            return True
        else:
            return False
        
    @staticmethod
    def get_by_int(code: int) -> "CommandStatusCode.CODE":
        if CommandStatusCode.is_server_code(code) or CommandStatusCode.is_client_code(code):
            return code
        else:
            return CommandStatusCode.SERVER_INTERNAL_ERROR
        
    @staticmethod
    def is_ok(code: int) -> bool:
        if code == CommandStatusCode.SERVER_OK or code == CommandStatusCode.SERVER_CREATED or code == CommandStatusCode.CLIENT_OK:
            return True
        else:
            return False
    
    @staticmethod
    def is_error(code: int) -> bool:
        if code > 200 and code != CommandStatusCode.CLIENT_OK:
            return True
        else:
            return False