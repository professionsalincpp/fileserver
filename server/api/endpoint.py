from http import HTTPMethod
from typing import Union
from utils.stringutils import tostr


class APIPath:
    def __init__(self, name: str, description: str = None, parent: "APIPath" = None):
        self.name = name
        self.description = description if description else "No description"
        self.parent = parent

    @property
    def path(self):
        if self.parent is not None:
            return f"{self.parent.path}/{self.name}"
        else:
            return self.name

VALIDTYPES = Union[str, int, float, bool, list, dict, None]

class APIEndpoint(APIPath):
    def __init__(self, name: str, method: HTTPMethod, body_structure: dict = None,  parent: "APIPath" = None):
        super().__init__(name=name, parent=parent)
        self.method = method
        self.body_structure = body_structure

    def bodystr(self, body_structure: dict = None):
        if body_structure is None:
            body_structure = self.body_structure
        _dict = {}
        for key, value in body_structure.items():
            if isinstance(value, dict):
                _dict[key] = self.bodystr(value)
            elif isinstance(value, VALIDTYPES):
                _dict[key] = value
            else:
                _dict[key] = tostr(value)

        return _dict

    @property
    def body(self):
        if self.body_structure:
            return self.body_structure
        else:
            return {}

    @property
    def path(self):
        if self.parent is not None:
            return f"{self.parent.path}/{self.name}"
        else:
            return self.name
    
