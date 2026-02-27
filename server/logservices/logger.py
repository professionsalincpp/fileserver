import datetime
import logging
import sys
from .format import *
import os
from typing import Literal
from colorama import Fore, Style
from utils.pathutils import get_correct_path
try:
    from config import Config
except ImportError:
    print("Using without context logger")



def get_logger(name=None, level=logging.INFO):
    logger = logging.getLogger(name)
    if level == logging.ERROR:
        logging.basicConfig(level=logging.ERROR, format=f'{Fore.RED}Error in %(name):{Style.RESET_ALL} %(message)s')

    elif level == logging.CRITICAL:
        logging.basicConfig(level=logging.CRITICAL, format=f'{Fore.RED}Critical error in %(name):{Style.RESET_ALL} %(message)s')
    elif level == logging.WARNING:
        logging.basicConfig(level=logging.WARNING, format=f'{Fore.YELLOW}Warning in %(name):{Style.RESET_ALL} %(message)s')
    elif level == logging.INFO:
        logging.basicConfig(level=logging.INFO, format=f'{Fore.GREEN}Info in %(name):{Style.RESET_ALL} %(message)s',
                        datefmt=f'{Fore.GREEN}[%Y-%m-%d %H:%M:%S]{Style.RESET_ALL}')
    return logger

    
class MultiLogger:
    def __init__(self, name, log_to_file=True):
        self.logging_file_name = f"{name}.log"
        self.name = name
        self.setupped = True if not log_to_file else False

    def setup(self):
        """
        Creates the logging file if it doesn't exist.
        """
        
        self.extended_file_name = get_correct_path(Config.get_config()['log']['path'], self.logging_file_name)
        if not os.path.exists(os.path.dirname(self.extended_file_name)):
            self.setupped = False
            return
        if not os.path.exists(self.extended_file_name):
            with open(self.extended_file_name, 'w') as f:
                pass
        self.log_format = Config.LOG_FORMAT()
        print(f"Setupped logger {self.name} with format {self.log_format}")
        if self.log_format.lower() == "json":
            self.log_format = LogFormat.JSON
        elif self.log_format.lower() == "linux_terminal" or self.log_format.lower() == "terminal" or self.log_format.lower() == "linux":
            self.log_format = LogFormat.LINUX_TERMINAL_LIKE
        else:
            self.log_format = LogFormat.STANDART
        self.setupped = True

    def make_message(self, message, title, context, level: LogLevel, highlight=False):
        timestamp: str = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        log_obj = LogObject(timestamp, context, level, title + ": " + message)
        return format_log(log_obj, self.log_format, highlight)

    def critical(self, message, title=f"Critical", context=None):
        if title is not None:
            title = f"{Fore.RED}{title}{Style.RESET_ALL}"
        self.log(message, title, context, LogLevel.Critical)
    
    def error(self, message, title=f"Error", context=None):
        if title is not None:
            title = f"{Fore.RED}{title}{Style.RESET_ALL}"
        self.log(message, title, context, LogLevel.Error)        
    
    def warning(self, message, title=f"Warning", context=None):
        if title is not None:
            title = f"{Fore.YELLOW}{title}{Style.RESET_ALL}"
        self.log(message, title, context, LogLevel.Warning)

    def info(self, message, title="Info", context=None):
        self.log(message, title, context, LogLevel.Info)

    def success(self, message, title="Success", context=None):
        title = f"{Fore.GREEN}{title}{Style.RESET_ALL}"
        self.log(message, title, context, LogLevel.Success)

    def cleanup_message_for_file(self, message):
        for ansi_color in [Fore.RED, Fore.YELLOW, Fore.GREEN, Fore.WHITE]:
            message = message.replace(ansi_color, "")
        for ansi_style in [Style.RESET_ALL, Style.BRIGHT]:
            message = message.replace(ansi_style, "")
        return message

    def log(self, message, title, context, type: Literal["critical", "error", "warning", "info", "success"] = "info"):
        if not self.setupped:
            self.setup()
        if not self.setupped:
            print("Error: Logging file not setupped")
            return
        if context is None:
            context = self.name
        with open(self.extended_file_name, 'a') as f:
            clean_msg: str = self.cleanup_message_for_file(self.make_message(message, title, context, type, highlight=False))
            f.write(clean_msg)

        sys.stdout.write(self.make_message(message, title, context, type, highlight=True))
        