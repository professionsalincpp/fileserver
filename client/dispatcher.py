import argparse
import base64
from services.file_system.image_viewer import ImageViewer
from model.response import CommandResponse
import json
from logger import MultiLogger
from commands.createfile import CreateFileCommand
from commands.read import ReadCommand
from commands.download import DownloadCommand
from commands.setup import SetupCommand
from commands.upload import UploadCommand
from commands.move import MoveCommand
from commands.copy import CopyCommand
from commands.createdir import CreateDirCommand
import os
from config import Config
from services.file_system.file_viewer import FileViewer
from messages import *
from PIL import Image
from services.encoder import Encoder
from io import BytesIO

_logger = MultiLogger("dispatcher")

class Dispatcher:
    def __init__(self, args):
        self.args = args


    def dispatch(self):
        name: str = f"_dispatch_{self.args.subcmd}"
        if self.args.subcmd == "create":
            if self.args.create_type == "file":
                name = "_dispatch_create_file"
            elif self.args.create_type == "dir":
                name = "_dispatch_create_dir"
        if not hasattr(self, name):
            _logger.error(f"Invalid subcommand \"{self.args.subcmd}\"", context="dispatch")
            return
        method = getattr(self, name)
        method(self.args)

    def _dispatch_upload(self, args: argparse.Namespace) -> None:
        if not args.file:
            _logger.error("No file specified", context="dispatch_upload")
            return
        cmd = UploadCommand(args.file, Config().get_server_url())
        response = cmd.execute()
        if response.status_code == 200:
            _logger.info(f"File \"{args.file}\" uploaded successfully", context="dispatch_upload")
        self.print_response("upload", response)
    
    def _dispatch_setup(self, args: argparse.Namespace) -> None:
        cmd = SetupCommand(args.host, args.port)
        if cmd.execute():
            _logger.info("Setup successful", context="dispatch_setup")
        else:
            _logger.error("Failed to setup", context="dispatch_setup")

    def _dispatch_read(self, args: argparse.Namespace) -> None:
        if not args.file:
            _logger.error("No file specified", context="dispatch_read")
            return
        cmd = ReadCommand(args.file, Config().get_server_url())
        result = cmd.execute()
        if result.status_code == 200:
            json_data = json.loads(result.data)
            mimetype = json_data["data"]["mimetype"]
            if mimetype in ["image/jpeg", "image/png", "image/bmp", "image/gif"]:
                encoded_data = Encoder.encode(json_data["data"]["data"], mimetype)
                bytes_io = BytesIO(encoded_data)
                img = Image.open(bytes_io)
                viewer = ImageViewer(img)
                viewer.run()
            else:
                viewer = FileViewer(json_data["data"]["data"])
                viewer.run()
        self.print_response("read", result)

    def _dispatch_move(self, args: argparse.Namespace) -> None:
        if not args.source or not args.dest:
            _logger.error("No source or destination specified", context="dispatch_move")
            return
        cmd = MoveCommand(args.source, args.dest, Config().get_server_url())
        result = cmd.execute()
        self.print_response("move", result)

    def _dispatch_copy(self, args: argparse.Namespace) -> None:
        if not args.source or not args.dest:
            _logger.error("No source or destination specified", context="dispatch_copy")
            return
        cmd = CopyCommand(args.source, args.dest, Config().get_server_url())
        result = cmd.execute()
        self.print_response("copy", result)

    def _dispatch_create_dir(self, args: argparse.Namespace) -> None:
        if not args.directory:
            _logger.error("No directory specified", context="dispatch_createdir")
            return
        cmd = CreateDirCommand(args.directory, Config().get_server_url())
        result = cmd.execute()
        self.print_response("createdir", result)

    def _dispatch_create_file(self, args: argparse.Namespace) -> None:
        if not args.file:
            _logger.error("No file specified", context="dispatch_createfile")
            return
        cmd = CreateFileCommand(args.file, Config().get_server_url())
        result = cmd.execute()
        self.print_response("createfile", result)

    def _dispatch_download(self, args: argparse.Namespace) -> None:
        if not args.file:
            _logger.error("No file specified", context="dispatch_download")
            return
        cmd = DownloadCommand(args.file, Config().get_server_url())
        result = cmd.execute()
        self.print_response("download", result)

    def print_response(self, command: str, response: CommandResponse):
        table = [
            ["Command", command],
            ["Status Code", format_server_status(response.status_code)],
        ]
        try:
            data_json = json.loads(response.data)
        except Exception as e:
            _logger.error(f"Failed to parse response data: {e}", context="print_response")
            return
        table.append(["Status", data_json["status"]])
        if CommandStatusCode.is_ok(response.status_code):
            table.append(["Message", data_json["message"]])
        else:
            table.append(["Error Code", str(data_json["error_code"])])
            table.append(["Message", data_json["message"]]),
            table.append(["Error Message", data_json["error_message"]])

        print_table(table)