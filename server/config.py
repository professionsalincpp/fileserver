import configparser
import os
import sys
from colorama import Fore, Style

CONFIG_LOADED: bool = False

_congig_hierarchy = {
    "server": ["host", "port"],
    "path": ["data", "templates"],
    "log": ["path", "format"],
}


def load_config(file: str) -> None:
    global CONFIG_LOADED
    if not os.path.exists(file):
        print(f"{Fore.RED}Fatal error{Style.RESET_ALL}: Config file \"{file}\" does not exist")
        sys.exit(1)
    if not Config.config:
        Config.config = configparser.ConfigParser()
        Config.config.read(file)
        if not check_config_is_valid(Config.config):
            print(f"{Fore.RED}Fatal error{Style.RESET_ALL}: Config file \"{file}\" is not valid")
            sys.exit(1)
        CONFIG_LOADED = True
        print(f"{Fore.GREEN}Success{Style.RESET_ALL}: Config file \"{file}\" loaded successfully")
    else:
        print(f"{Fore.GREEN}Warning{Style.RESET_ALL}Warning: Config file \"{file}\" already loaded. Using existing config object.")
    


def check_config_is_valid(config: "configparser.ConfigParser"):
    # check if all required sections are present
    # check if all required keys are present
    for section in _congig_hierarchy.keys():
        if section not in config.sections():
            print(f"{Fore.RED}Fatal error{Style.RESET_ALL}: Missing section \"{section}\" in config file")
            return False
    for section, keys in _congig_hierarchy.items():
        for key in keys:
            if key not in config[section]:
                print(f"{Fore.RED}Fatal error{Style.RESET_ALL}: Missing key \"{key}\" in section \"{section}\" in config file")
                return False
    return True

def require_config(func):
    def wrapper(*args, **kwargs):
        if not CONFIG_LOADED:
            print(f"{Fore.RED}Fatal error{Style.RESET_ALL}: Config file is not loaded, cannot run function \"{func.__name__}\"")
            sys.exit(1)
        return func(*args, **kwargs)
    return wrapper


class Config:
    config: "configparser.ConfigParser" = None
    
    @require_config
    def SERVER_HOST():
        return Config.get_config()['server']['host']
    
    @require_config
    def SERVER_PORT():
        return Config.get_config()['server']['port']
    
    
    @require_config
    def PATH_DATA():
        return Config.get_config()['path']['data']
    

    @require_config
    def PATH_TEMPLATES():
        return Config.get_config()['path']['templates']
    

    @require_config
    def LOG_PATH():
        return Config.get_config()['log']['path']
    

    @require_config
    def LOG_FORMAT():
        return Config.get_config()['log']['format']
    
    
    @classmethod
    def get_config(cls):
        return cls.config

