""" 
Copy Command Class
Represents an upload command that sends data to a server.

Attributes:

path (str): The path where the data will be uploaded.
data (dict): The data to be uploaded.
server_url (str): The URL of the server where the data will be uploaded.
Methods:

__init__(data: dict, server_url: str) -> None
Initializes the upload command with the given data and server URL.

execute() -> CommandResponse
Executes the upload command and returns a CommandResponse object.

Copy Process:

Checks if both path and data are present. If not, returns an error response.
Creates a POST request with the data, path, and hash.
Sends the request to the server and checks the response status code.
Returns a CommandResponse object based on the response status code.
Response Status Codes:

CommandStatusCode.SUCCESS: The upload was successful.
CommandStatusCode.INVALID_DATA: The upload command requires both path and data.
CommandStatusCode.ERROR: An error occurred during the upload process.
ServerStatusCode.FILE_NOT_FOUND: The file was not found on the server.
ServerStatusCode.INTERNAL_ERROR: An internal error occurred on the server.
Exceptions:

Any exception that occurs during the upload process will be caught and returned as a CommandResponse object with a CommandStatusCode.ERROR status code.

Writen by: professionsalincpp on 07.07.2025
"""

from model.command import Command
import requests
from model.response import CommandResponse
from model.statuscodes import CommandStatusCode
from services.requestsender import Sender
from http import HTTPMethod


class CopyCommand(Command):
    """
    Copy command class
    """
    def __init__(self, source_path: str, dest_path: str, server_url: str) -> None:
        self.source_path = source_path
        self.dest_path = dest_path
        self.server_url = server_url

    def execute(self) -> CommandResponse:
        post_data = {
            "path": {
                "source": self.source_path,
                "dest": self.dest_path                
            }
        }

        response: requests.Response = Sender.send(post_data, self.server_url + "/api/copy", HTTPMethod.PUT)
        return CommandResponse(response.text, CommandStatusCode.get_by_int(response.status_code))



        