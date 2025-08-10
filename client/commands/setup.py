import os
from colorama import Fore, Style
from configparser import ConfigParser
from model.response import CommandResponse
from model.statuscodes import CommandStatusCode
from model.command import Command
from services.fileprocessor import FileProcessor

class SetupCommand(Command):
    def __init__(self, data: dict, is_gui: bool=False) -> None:
        self.host = data.get("host")
        self.port = str(data.get("port"))
        self.is_gui = is_gui

    def execute(self) -> CommandResponse:
        parser = ConfigParser()
        if not self.is_gui:
            if not (self.host or self.port):
                return CommandResponse("Host and port arguments are required, please run the setup command again with the host and port arguments, or run the setup command with the --gui argument", status_code=CommandStatusCode.INVALID_DATA)
            if not FileProcessor.file_exists("config.ini"):
                return self.gui_setup(parser)
            parser.read("config.ini")                
            if self.host:
                parser.set("server", "host", self.host)
            elif not parser.get("server", "host"):
                return CommandResponse("Host argument is required, please run the setup command again with the host argument", status_code=CommandStatusCode.INVALID_DATA)
            if self.port != "None":
                parser.set("server", "port", self.port)
            elif not parser.get("server", "port"):
                parser.set("server", "port", "8080")
            with open("config.ini", "w") as f:
                parser.write(f)
        else:
            return self.gui_setup(parser)
        return CommandResponse("Setup successful", status_code=CommandStatusCode.CLIENT_OK)
    
    def gui_setup(self, parser: ConfigParser):
        """
        Interactive GUI setup for configuring the server host and port.

        This method clears the console screen and prompts the user to enter the
        host and port for the server. If the user does not provide a port, the
        default port '8080' is used. The provided host and port are saved to the
        'config.ini' file under the 'server' section. If the 'server' section
        does not exist, it is created.

        Args:
            parser (ConfigParser): The configuration parser used to read and
            write the 'config.ini' file.

        Returns:
            CommandResponse: A response indicating success or failure of the
            setup process. Returns an error if the host is not provided.
        """

        os.system("cls")
        print(f"{Fore.WHITE}setup@setuphelper ~ GUI Setup v1.0{Style.RESET_ALL}")
        host = input(f"{Fore.WHITE}setup@setuphelper ~ Enter the host of the server: {Style.RESET_ALL}{Fore.CYAN}")
        if not host:
            return CommandResponse("Host argument is required, please run the setup command again with the host argument", status_code=CommandStatusCode.INVALID_DATA)
        port = input(f"{Fore.WHITE}setup@setuphelper ~ Enter the port of the server: {Style.RESET_ALL}{Fore.CYAN}None\b\b\b\b")
        if not parser.has_section("server"):
            parser.add_section("server")
        if not port:
            parser.set("server", "port", "8080")
        else:
            parser.set("server", "port", port)
        parser.set("server", "host", host)
        with open("config.ini", "w") as f:
            parser.write(f)
        return CommandResponse("Setup successful", status_code=CommandStatusCode.CLIENT_OK)