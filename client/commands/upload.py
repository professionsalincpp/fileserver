""" 
Upload Command Class
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

Upload Process:

Checks if both path and data are present. If not, returns an error response.
Calculates the content length and SHA-256 hash of the data.
Creates a POST request with the data, path, and hash.
Sets the Content-Length header with the calculated content length.
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

import hashlib
from http import HTTPMethod
from typing import Any
from services.fileprocessor import FileProcessor
from model.command import Command
import requests
from model.response import CommandResponse
from model.statuscodes import CommandStatusCode
from services.requestsender import Sender
import mimetypes
import os
from services.encoder import Encoder
import services.extendedmimes as extendedmimes

class UploadCommand(Command):
    """
    Upload command class
    """
    def __init__(self, path: str, server_url: str) -> None:
        self.path = path
        self.server_url = server_url

    def execute(self) -> CommandResponse:
        self.data = FileProcessor.read_file(self.path)
        if not self.data:
            return CommandResponse("File not found", CommandStatusCode.CLIENT_FILE_NOT_FOUND)
        
        data_hash = hashlib.sha256(self.data).hexdigest()
        mimetype = extendedmimes.guess_mimetype(self.path)
        data = Encoder.decode(self.data, mimetype)
        slice1 = data[:300]
        slice2 = self.data[:300]
        print(f"Actual data: {slice2}")
        print(f"Decoded data: {slice1}")
        print(len(slice1))
        print(len(slice2))

        post_data = {
            'path': os.path.basename(self.path),
            'data': data,
            'hash': data_hash,
        }

        response: requests.Response = Sender.send(post_data, self.server_url + '/api/write', HTTPMethod.PUT)
        return CommandResponse(response.text, CommandStatusCode.get_by_int(response.status_code))



        