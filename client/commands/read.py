"""
Read command

Writen by professionsalincpp on 16.07.2025
"""

from model.command import Command
import requests
from model.response import CommandResponse
from model.statuscodes import CommandStatusCode
from services.requestsender import Sender


class ReadCommand(Command):
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
        return CommandResponse(response.text, CommandStatusCode.get_by_int(response.status_code))

