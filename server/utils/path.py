import os
import re
import sys
import pathlib

def get_absolute_path(path: str, root: str) -> str:
    res = os.path.normpath(os.path.join((root), (path)))
    return res

def check_is_relative(path: str) -> bool:
    if re.match(r'^[a-zA-Z]:', path):
        return False
    else:
        return True
    

def get_executable_dir() -> str:
    dirname = pathlib.Path(sys.modules['__main__'].__file__).resolve().parent
    if getattr(sys, 'frozen', False):
        # moves two levels up
        try:
            dirname = dirname.parent.parent
        except:
            print("Failed to get the absolute path of the executable main.exe.")
    return dirname


def get_correct_path(templates_path: str, path: str) -> str:
    dirname = get_executable_dir()    
    if check_is_relative(templates_path):
        return get_correct_path(get_absolute_path(templates_path, dirname), path)
    else:
        return os.path.normpath(os.path.join(templates_path, path))