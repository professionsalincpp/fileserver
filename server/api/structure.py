from api.endpoint import APIEndpoint

_valid_requests = {
    "write": {
        "path": str,
        "data": str,
        "hash": str
    },
    "read": {
        "path": str
    },
    "copy": {
        "path": {
            "source": str,
            "dest": str
        }
    },
    "move": {
        "path": {
            "source": str,
            "dest": str
        }
    },
    "create/dir": {
        "path": str
    },
    "create/file": {
        "path": str
    }
}

class APIStructure:
    def __init__(self, basepath: str, endpoints: list[APIEndpoint] = []):
        self.basepath = basepath.strip("/") if len(basepath) > 1 else "api"
        self.endpoints = endpoints

    def add_endpoint(self, endpoint: APIEndpoint):
        self.endpoints.append(endpoint)
    
    def items(self):
        return [endpoint.body for endpoint in self.endpoints]
    
    def keys(self):
        return ["%s#%s" % (endpoint.path, endpoint.method) for endpoint in self.endpoints] # ["endpoint.name for endpoint in self.endpoints]

    def dict(self):
        _dict =  {
            "basepath": self.basepath,
            "endpoints": [{
                "path": endpoint.path,
                "method": endpoint.method,
                "body": endpoint.bodystr()}
                for endpoint in self.endpoints]
        }
        return _dict
    
    def find(self, path: str) -> APIEndpoint:
        for endpoint in self.endpoints:
            print(endpoint.path, path)
            if endpoint.path == path or "/" + endpoint.path == path:
                return endpoint
            
    def validate(self, path: str, request: dict, endpoint_body: dict =None) -> bool:
        if not endpoint_body:
            endpoint_body = self.find(path)
            if not endpoint_body:
                return False
            endpoint_body = endpoint_body.body
        for key, value in endpoint_body.items():
            if key not in request.keys():
                return False
            if isinstance(value, dict):
                if not isinstance(request[key], dict): return False
                is_valid = self.validate(path, request[key], endpoint_body[key])
                if not is_valid: return False
            else:
                reqvalue = request[key]
                if not isinstance(reqvalue, value):
                    print(f"Type mismatch for {key} in {path}! Expected {value}, got {type(reqvalue)}")
                    print(reqvalue)
                    print(value)
                    return False

        return True
                
