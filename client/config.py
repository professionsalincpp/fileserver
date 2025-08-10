import configparser
from logger import MultiLogger
import sys

_logger = MultiLogger("config")

class Config:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')
        self.host = self.try_get_config("server", "host")
        self.port = self.try_get_config("server", "port")

    def update(self):
        self.config.read('config.ini')
        self.host = self.try_get_config("server", "host")
        self.port = self.try_get_config("server", "port")

    def try_get_config(self, section: str, key: str) -> str:
        if self.config.has_option(section, key):
            return self.config.get(section, key)
        else:
            return 'unknown'

    def check_config_is_valid(self) -> bool:
        if self.host == 'unknown' or self.port == 'unknown':
            return False
        return True

    def get_server_url(self) -> str:
        if self.host == 'unknown' or self.port == 'unknown':
            _logger.error("Host or port is unknown, please run the setup command first", title="Error", context="error")
            sys.exit(1)
        url: str = ""
        if url.startswith("http://") or url.startswith("https://"):
            return url
        else:
            return f"http://{self.host}:{self.port}"