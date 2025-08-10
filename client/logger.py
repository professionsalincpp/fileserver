import os
from typing import Literal
from colorama import Fore, Style

    
class MultiLogger:
    def __init__(self, name):
        self.name = name
        self.fore_associations = {
            "critical": Fore.RED,
            "error": Fore.RED,
            "warning": Fore.YELLOW,
            "info": Fore.WHITE,
            "success": Fore.GREEN
        }


    def make_message(self, message, title, context, type: Literal["critical", "error", "warning", "info", "success"] = "info"):
        return f"{self.fore_associations[type]}{self.name}@{context}{Style.RESET_ALL} ~ {title}: {message}"

    def critical(self, message, title=f"Critical", context="critical"):
        title = f"{Fore.RED}{title}{Style.RESET_ALL}"
        self.log(self.make_message(message, title, context, "critical"))
    
    def error(self, message, title=f"Error", context="error"):
        title = f"{Fore.RED}{title}{Style.RESET_ALL}"
        self.log(self.make_message(message, title, context, "error"))
    
    def warning(self, message, title=f"Warning", context="warning"):
        title = f"{Fore.YELLOW}{title}{Style.RESET_ALL}"
        self.log(self.make_message(message, title, context, "warning"))

    def info(self, message, title="Info", context="info"):
        title = f"{Fore.WHITE}{title}{Style.RESET_ALL}"
        self.log(self.make_message(message, title, context, "info"))

    def success(self, message, title="Success", context="success"):
        title = f"{Fore.GREEN}{title}{Style.RESET_ALL}"
        self.log(self.make_message(message, title, context, "success"))

    def cleanup_message_for_file(self, message):
        """
        Cleans up ansi colors and formatting for logging to file.
        """
        for ansi_color in [Fore.RED, Fore.YELLOW, Fore.GREEN, Fore.WHITE]:
            message = message.replace(ansi_color, "")
        for ansi_style in [Style.RESET_ALL, Style.BRIGHT]:
            message = message.replace(ansi_style, "")
        return message
    

    def log(self, message):
        print(message)
        