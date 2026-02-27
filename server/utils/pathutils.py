import os
import re
import sys
from pathlib import Path
from config import Config as cfg

DATA_PATH = None
TEMPLATES_PATH = None
HTML_PATH = None
SCRIPTS_PATH = None
CSS_PATH = None
BOOTSTRAP_PATH = None


PATHS_LOADED = False

def init_paths():
    global DATA_PATH, TEMPLATES_PATH, HTML_PATH, SCRIPTS_PATH, PATHS_LOADED, BOOTSTRAP_PATH, CSS_PATH
    DATA_PATH = Path(cfg.PATH_DATA())
    TEMPLATES_PATH = Path(cfg.PATH_TEMPLATES())
    HTML_PATH = TEMPLATES_PATH / 'html'
    SCRIPTS_PATH = TEMPLATES_PATH / 'scripts'
    CSS_PATH = TEMPLATES_PATH / 'css'
    BOOTSTRAP_PATH = CSS_PATH / 'bootstrap-material-design-master'
    PATHS_LOADED = True

def get_absolute_path(path: str, root: str='.') -> str:
    if root == '.':
        root = os.getcwd()
    res = Path(root).joinpath(path).resolve()
    # Deprecated using pathlib instead
    return str(res)

def check_is_relative(path: str) -> bool:
    if re.match(r'^[a-zA-Z]:', path):
        return False
    else:
        return True
    

def get_executable_dir() -> str:
    dirname = Path(sys.modules['__main__'].__file__).resolve().parent
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
        templates_path = get_absolute_path(templates_path, dirname)
    
    res = Path(templates_path).joinpath(path).resolve()
    return str(res)

def find_in_default_paths(file_name: str) -> str | None:
    # Trying to find the file in HTML_PATH, SCRIPTS_PATH and TEMPLATES_PATH
    if not PATHS_LOADED:
        init_paths()
    file_path = get_correct_path(str(HTML_PATH), file_name)
    if os.path.isfile(file_path):
        return file_path
    for path in [SCRIPTS_PATH, TEMPLATES_PATH, CSS_PATH, BOOTSTRAP_PATH]:
        
        file_path = get_correct_path(str(path), file_name)
        if os.path.isfile(file_path):
            return file_path
        
    file_path = get_correct_path(str(HTML_PATH), file_name + ".html")
    if os.path.isfile(file_path):
        return file_path
    return None