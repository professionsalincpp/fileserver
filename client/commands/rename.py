"""
Rename command

Writen by professionsalincpp on 16.07.2025
"""

from http import HTTPMethod
import mimetypes
from model.command import Command
import requests
from model.response import CommandResponse
from model.statuscodes import CommandStatusCode
from services.requestsender import Sender
from services.fileprocessor import FileProcessor
from services.encoder import Encoder


class RenameCommand(Command):
    """
    Rename command class
    """
    def __init__(self, old_path: str, new_path: str, server_url: str) -> None:
        self.old_path = old_path
        self.new_path = new_path
        self.server_url = server_url

    def execute(self) -> CommandResponse:
        post_data = {
            "path": {
                "old": self.old_path,
                "new": self.new_path
            }
        }

        print(post_data)

        response: requests.Response = Sender.send(post_data, self.server_url + "/api/rename", HTTPMethod.PUT)
        
        return CommandResponse(response.text, CommandStatusCode.get_by_int(response.status_code))

