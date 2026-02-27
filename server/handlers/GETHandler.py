import os
from config import Config
from fileservices.fileworkerstatus import FileWorkerStatus
import utils.pathutils as pathutils
from typing import List
from fileservices.fileworker import FileWorker, FileWorkerMode
from utils.pathutils import get_correct_path
from handlers.BaseHandler import BaseHandler
from fileservices.nameprovider import NameProvider
from fileservices.providerresult import ProviderResult
from fileservices.providerstatus import ProviderStatus
from utils.stringutils import strpath
from .response import Response
from api import basic_structure


class GETHandler(BaseHandler):
    @classmethod
    def processpath(cls, path: List[str]) -> Response:
        if path[0] == "file":
            return cls.processfile(path[1:])
        elif path[0] == "api" and len(path) >= 2 and path[1] == "structure":
            return cls.processapistructure(path[2:])
        elif path[0] == "list" and len(path) >= 2 and path[1] == "dir":
            return cls.processlistdir(path[2:])
        else:
            return cls.processpage(path)
    
    @classmethod
    def processpage(cls, path: List[str]) -> Response:
        if len(path) == 1 and path[0] == "":
            path = ["index.html"]
        filepath = pathutils.find_in_default_paths(strpath(path))
        if filepath is None:
            print("Warning: Page not found")
            return cls.wrap_error(404, "Not Found", "Not Found")

        fileworker = FileWorker(filepath, FileWorkerMode.READ)
        fileworker.run()
        
        if fileworker.get_result().status == FileWorkerStatus.SUCCESS:
            return Response(fileworker.get_result().data.getvalue(), 200)
        else:
            return Response(fileworker.get_result().data.getvalue(), 500)
        
    @classmethod
    def processfile(cls, path: List[str]) -> Response:
        filepath = pathutils.get_absolute_path(strpath(path), Config.PATH_DATA())
        if os.path.isdir(filepath):
            resp = f"<h1>Index of /{'/'.join(path)}</h1><br>"
            for file in os.listdir(filepath):
                resp += f"<a href=\"/file/{'/'.join(path)}/{file}\">{file}</a><br>"
            
            return Response(resp.encode(), 200)
        fileworker = FileWorker(filepath, FileWorkerMode.READ)
        fileworker.run()

        work_result = fileworker.get_result()
        if work_result.status == FileWorkerStatus.SUCCESS:
            return Response(work_result.data.getvalue(), 200)
        elif work_result.status == FileWorkerStatus.NOT_FOUND:
            return Response(work_result.data.getvalue(), 404)
        else:
            return Response(work_result.data.getvalue(), 500)
        
    @classmethod
    def processlistdir(cls, path: List[str]) -> Response:
        filepath = get_correct_path(Config.get_config()['path']['data'], "/".join(path))
        result: ProviderResult = NameProvider.listdir(filepath)
        if result.status == ProviderStatus.SUCCESS:
            return Response(cls.as_json({
                "status": "success",
                "message": "List of files",
                "data": result.data,
                "type": result.type,
            }), 200)
        elif result.status == ProviderStatus.NOT_FOUND:
            return cls.wrap_error(404, "Not Found", "Not Found")
        else:
            return cls.wrap_error(500, "Internal Server Error", "Internal Server Error")
        
    @classmethod
    def processapistructure(cls, path: List[str]) -> Response:
        if len(path) == 0 or path[0] == "":
            print(basic_structure)
            return cls.wrap_success(200, "API structure", basic_structure.dict())
        else:
            if basic_structure.find(strpath(path)):
                endpoint = basic_structure.find(strpath(path))
                return cls.wrap_success(200, "API structure", {"endpoint": endpoint.path, "description": endpoint.description, "method": endpoint.method, "body": endpoint.bodystr()})
            else:
                return cls.wrap_error(404, "API structure not found", f"API structure not found for path {path}")