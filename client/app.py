import os
import argparse
from colorama import Fore, Style
from commands.setup import SetupCommand
from logger import MultiLogger
import os
from commands.upload import UploadCommand
from config import Config
import sys
from dispatcher import Dispatcher

_logger = MultiLogger("client")

# add subcommand [upload] to upload file to server
conf = Config()

def parse_args():
    parser = argparse.ArgumentParser(description="File Server")
    subparsers = parser.add_subparsers(dest="subcmd")

    upload_parser = subparsers.add_parser("upload", help="Upload file to server")
    upload_parser.add_argument("file", type=str, help="File to upload")

    setup_parser = subparsers.add_parser("setup", help="Setup server")
    setup_parser.add_argument("--host", type=str, help="Host to setup server on", default=None)
    setup_parser.add_argument("--port", type=int, help="Port to setup server on", default=None)
    setup_parser.add_argument("--gui", action="store_true", help=f"Use GUI for setup, {Fore.YELLOW}WARNING: This will clear the console{Style.RESET_ALL}", default=False)

    copy_parser = subparsers.add_parser("copy", help="Copy file")
    copy_parser.add_argument("source", type=str, help="Source file path to copy")
    copy_parser.add_argument("dest", type=str, help="Destination path to copy")

    move_parser = subparsers.add_parser("move", help="Move file")
    move_parser.add_argument("source", type=str, help="Source file path to move")
    move_parser.add_argument("dest", type=str, help="Destination path to move")

    create_parser = subparsers.add_parser("create", help="Create file or directory")
    create_subparsers = create_parser.add_subparsers(dest="create_type")
    create_dir_parser = create_subparsers.add_parser("dir", help="Creates directory")
    create_dir_parser.add_argument("directory", type=str, help="Directory name or path")

    create_file_parser = create_subparsers.add_parser("file", help="Creates file")
    create_file_parser.add_argument("file", type=str, help="File name or path")

    read_parser = subparsers.add_parser("read", help="Read file")
    read_parser.add_argument("file", type=str, help="File to read")

    download_parser = subparsers.add_parser("download", help="Download file")
    download_parser.add_argument("file", type=str, help="File to download")

    delete_parser = subparsers.add_parser("delete", help="Delete file")
    delete_parser.add_argument("file", type=str, help="File or directory to delete")

    rename_parser = subparsers.add_parser("rename", help="Rename file or directory")
    rename_parser.add_argument("old_path", type=str, help="File or directory to rename")
    rename_parser.add_argument("new_path", type=str, help="New name for file or directory")
        
    print_config_parser = subparsers.add_parser("print_config", help="Prints the current configuration")

    return parser.parse_args()

    
def check_config():
    if not conf.check_config_is_valid():
        _logger.error("Configuration file is not valid, please run the setup command", context="main")
        sys.exit(1)          

def main():
    args = parse_args()
    if args.subcmd != "setup":
        check_config()
    Dispatcher(args).dispatch()

if __name__ == "__main__":
    main()