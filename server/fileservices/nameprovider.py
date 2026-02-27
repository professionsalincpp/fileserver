import os
from config import Config
import utils.pathutils as pathutils
from .providerresult import ProviderResult
from .providerstatus import ProviderStatus


class NameProvider:
    @classmethod
    def listdir(cls, path: str) -> list[str]:
        path = pathutils.get_correct_path(Config.get_config()['path']['data'], path)
        if os.path.isdir(path):
            _listdir = os.listdir(path)
            for i in range(len(_listdir)):
                if os.path.isdir(os.path.join(path, _listdir[i])):
                    is_empty = False
                    if len(os.listdir(os.path.join(path, _listdir[i]))) == 0:
                        is_empty = True
                    _listdir[i] = {
                        'name': _listdir[i],
                        'path': os.path.join(path, _listdir[i]),
                        'type': 'directory',
                        'is_empty': is_empty
                    }
                else:
                    _listdir[i] = {
                        'name': _listdir[i],
                        'path': os.path.join(path, _listdir[i]),
                        'type': 'file'
                    }
            return ProviderResult(_listdir, ProviderStatus.SUCCESS, "directory")
        elif os.path.isfile(path):
            return ProviderResult({
                'name': os.path.basename(path),
                'path': path
            }, ProviderStatus.SUCCESS, "file")
        else:
            return ProviderResult({
                
            }, ProviderStatus.NOT_FOUND)