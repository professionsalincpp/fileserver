"""
Read command

Writen by professionsalincpp on 16.07.2025
"""

import mimetypes
from model.command import Command
import requests
from model.response import CommandResponse
from model.statuscodes import CommandStatusCode
from services.requestsender import Sender
from services.fileprocessor import FileProcessor
from services.encoder import Encoder


class DownloadCommand(Command):
    """
    Read command class
    """
    def __init__(self, path: str, server_url: str) -> None:
        self.path = path
        self.server_url = server_url

    def execute(self) -> CommandResponse:
        post_data = {
            "path": self.path,
        }

        response: requests.Response = Sender.send(post_data, self.server_url + "/api/read")
        json_data = response.json()
        data = json_data["data"]["data"]
        mimetype = json_data["data"]["mimetype"]
        encoded_data = Encoder.encode(data, mimetype)
        FileProcessor.write_file(self.path, encoded_data)
        return CommandResponse(response.text, CommandStatusCode.get_by_int(response.status_code))

