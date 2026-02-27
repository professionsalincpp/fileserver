import io
import os
from typing import List
import urllib.parse
from http.server import BaseHTTPRequestHandler
from handlers.PUTHandler import PUTHandler
from handlers.GETHandler import GETHandler
from handlers.DELETEHandler import DELETEHandler
from handlers.response import Response
import json
from handlers.POSTHandler import POSTHandler
from logservices.logger import MultiLogger

__version__ = "0.0.1"
_logger = MultiLogger("request_handler")

class FileServerRequestHandler(BaseHTTPRequestHandler):

    """Simple HTTP request handler with GET and HEAD commands.

    This serves files from the current directory and any of its
    subdirectories.  The MIME type for files is determined by
    calling the .guess_type() method.

    The GET and HEAD requests are identical except that the HEAD
    request omits the actual contents of the file.

    """

    server_version = "FileServer/" + __version__
    index_pages = ("index.html", "index.htm")
    extensions_map = {
        '.gz': 'application/gzip',
        '.Z': 'application/octet-stream',
        '.bz2': 'application/x-bzip2',
        '.xz': 'application/x-xz',
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".png": "image/png",
        ".gif": "image/gif",
        ".js": "application/javascript",
        ".css": "text/css",
        ".html": "text/html",
        ".py": "text/x-python",
    }

    def __init__(self, *args, directory=None, **kwargs):
        if directory is None:
            directory = os.getcwd()
        self.directory = os.fspath(directory)
        super().__init__(*args, **kwargs)


    def log_request(self, code = "-", size = "-"):
        _logger.info(f"{self.requestline}", title="Request", context="request")
        _logger.info(f"{self.address_string()}", title="Client IP", context="request")
        code_description = {
            200: "OK",
            201: "Created",
            400: "Bad Request",
            404: "Not Found",
            403: "Permission Denied",
            500: "Internal Server Error"
        }
        _logger.info(f"{code} [{code_description.get(code, 'Unknown')}] {size}", title="Response", context="response")

    def log_error(self, format, *args):
        if args:
            _logger.error(format % args, title="Error", context="request")
        else:
            _logger.error(format, title="Error", context="request")

    def do_GET(self):
        """Serve a GET request."""
        path = self.translate_path()
        
        result: Response = GETHandler.processpath(path)
        self.send_full_response(result)

    def do_POST(self):
        path = self.translate_path()
        data = self.exract_data()

        result: Response = POSTHandler.processrequest(data, path)
        self.send_full_response(result)

    def do_PUT(self):
        path = self.translate_path()
        data = self.exract_data()

        result: Response = PUTHandler.processrequest(data, path)
        self.send_full_response(result)

    def do_DELETE(self):
        path = self.translate_path()
        data = self.exract_data()
        
        result: Response = DELETEHandler.processrequest(data, path)
        self.send_full_response(result)
        
    def is_json_exportable(self, obj):
        try:
            json.loads(obj)
            return True
        except:
            _logger.info(f"Object is not exportable to JSON", title="Error", context="request")
            _logger.info(f"{obj}", title="Object", context="request")
            return False
    
    def translate_path(self) -> List[str]:
        """Translate a /-separated PATH to the local filename syntax.

        Components that mean special things to the local file
        system (e.g. drive or directory names) are ignored.
        (XXX They should probably be diagnosed.)

        """
        # abandon query parameters
        path = self.path.split('?',1)[0]
        if path[0] == '/':
            path = path[1:]
        path = path.split('#',1)[0]
        path = path.lstrip('/')
        # Don't use posixpath; it doesn't work on Windows.
        path =  urllib.parse.unquote(path)
        return path.split('/')
        
    def translate_args(self) -> dict:
        if self.path.find('?') != -1:
            args = self.path.split('?',1)[1]
            args = urllib.parse.unquote(args)
            args = urllib.parse.parse_qs(args)
            return args
        else:
            return {}
        
    def send_headers(self, headers: dict):
        for header, value in headers.items():
            self.send_header(header, value)
        
    def send_full_response(self, response: Response):
        self.send_headers(response.headers)
        self.send_response(response.status_code)
        self.end_headers()
        self.wfile.write(response.body)

    def exract_data(self):
        raw_data = self.rfile.read(int(self.headers['Content-Length']))
        if self.headers['Content-Length'] == 0:
            data = {}
        elif self.is_json_exportable(raw_data):
            data = json.loads(raw_data)
        else:
            self.send_full_response(Response(b"Bad JSON data, must be valid JSON object or empty", 400))
            raise Exception("Bad JSON data, must be valid JSON object or empty")
        return data