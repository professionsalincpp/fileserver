from http.server import ThreadingHTTPServer, HTTPServer
from request_handler import FileServerRequestHandler
import socket
import os
from config import load_config, Config
from pathlib import Path
from utils.pathutils import get_absolute_path, get_executable_dir
import argparse
from logservices.logger import MultiLogger
from handlers.BaseHandler import BaseHandler

_logger = MultiLogger("server")
__version__ = "1.0.4"

def start_server(host="auto", port=8080):
    this_machine_ip = socket.gethostbyname(socket.gethostname())
    if host == "auto":
        host = this_machine_ip
    _logger.info(f"http://{this_machine_ip}:{port}", context="server", title="Server IP")
    _logger.info(f"Executable path: {get_executable_dir()}", context="server", title="Executable path")
    server_address = (this_machine_ip, port)
    BaseHandler.SERVER_URL = f"http://{this_machine_ip}:{port}"
    httpd = ThreadingHTTPServer(server_address, FileServerRequestHandler)
    httpd.serve_forever()

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', help='Path to configuration file', default=get_absolute_path("../config/config.ini", os.path.dirname(__file__)))
    parser.add_argument('--no-config', action='store_true', help='Do not load configuration file')
    parser.add_argument('--version', action='version', version=f'%(prog)s {__version__}')
    parser.add_argument('--host', help='Host to run the server on', default="auto")
    parser.add_argument('--port', type=int, help='Port to run the server on', default=0)
    parser.add_argument('--data', help='Path to data directory', default=get_absolute_path("../data", os.path.dirname(__file__)))
    
    # Add other command-line arguments as needed
    return parser.parse_args()


def main():
    args = parse_args()
    config_file = args.config
    
    print(f"Version: {__version__}")
    load_config(config_file)
    if args.host != "auto":
        Config.config['server']['host'] = args.host
    if args.port != 0:
        Config.config['server']['port'] = args.port
    if args.data != get_absolute_path("../data"):
        Config.config['path']['data'] = get_absolute_path(args.data)
    print("File:", config_file)
    print("Host:", Config.config['server']['host'])
    print("Port:", Config.config['server']['port'])
    print("Data:", Config.get_config()['path']['data'])


    # Use the configuration values from the file
    server_host = Config.get_config()['server']['host']
    server_port = int(Config.get_config()['server']['port']) #int(config['server']['port'])

    start_server(server_host, server_port)


if __name__ == '__main__':
    main()

