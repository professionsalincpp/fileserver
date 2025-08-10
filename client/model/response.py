""" 
Response Class

Represents a command response object with a standardized format.

Command response Format:

json
{
    "data": string,  // Response text
    "status_code": integer,  // HTTP status code
    "server_error_code": integer  // Error code (200 indicates no error)
}
Author: professionsalincpp Date: 07.07.2025 
"""

from dataclasses import dataclass

@dataclass
class CommandResponse:
    data: str
    status_code: int


 