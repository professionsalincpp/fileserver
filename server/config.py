import configparser
import os
import sys
from colorama import Fore, Style

_congig_hierarchy = {
    "server": ["host", "port"],
    "path": ["data", "templates"],
    "log": ["path", "format"],
}


def load_config(file: str) -> None:
    if not os.path.exists(file):
        print(f"{Fore.RED}config@load_config{Style.RESET_ALL} ~ {Fore.RED}Fatal error{Style.RESET_ALL}: Config file \"{file}\" does not exist")
        sys.exit(1)
    if not Config.config:
        Config.config = configparser.ConfigParser()
        Config.config.read(file)
        if not check_config_is_valid(Config.config):
            print(f"{Fore.RED}config@load_config{Style.RESET_ALL} ~ {Fore.RED}Fatal error{Style.RESET_ALL}: Config file \"{file}\" is not valid")
            sys.exit(1)
        print(f"{Fore.GREEN}config@load_config{Style.RESET_ALL} ~ {Fore.GREEN}Success{Style.RESET_ALL}: Config file \"{file}\" loaded successfully")
    else:
        print(f"{Fore.GREEN}config@load_config{Style.RESET_ALL} ~ {Fore.GREEN}Warning{Style.RESET_ALL}Warning: Config file \"{file}\" already loaded. Using existing config object.")
    


def check_config_is_valid(config: "configparser.ConfigParser"):
    # check if all required sections are present
    # check if all required keys are present
    for section in _congig_hierarchy.keys():
        if section not in config.sections():
            print(f"{Fore.RED}config@check_config_is_valid{Style.RESET_ALL} ~ {Fore.RED}Fatal error{Style.RESET_ALL}: Missing section \"{section}\"")
            return False
    for section, keys in _congig_hierarchy.items():
        for key in keys:
            if key not in config[section]:
                print(f"{Fore.RED}config@check_config_is_valid{Style.RESET_ALL} ~ {Fore.RED}Fatal error{Style.RESET_ALL}: Missing key \"{key}\" in section \"{section}\"")
                return False
    return True


class Config:
    config: "configparser.ConfigParser" = None
    @classmethod
    def get_config(cls):
        return cls.config

