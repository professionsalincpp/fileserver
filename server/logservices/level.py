from colorama import Fore
from dataclasses import dataclass


FOREASSOCIATIONS = {
    "critical": Fore.RED,
    "error": Fore.RED,
    "warning": Fore.YELLOW,
    "info": Fore.CYAN,
    "success": Fore.GREEN
}

class LogLevel:
    class Critical:
        value = "critical"
        fore = FOREASSOCIATIONS[value]

    class Error:
        value = "error"
        fore = FOREASSOCIATIONS[value]

    class Warning:
        value = "warning"
        fore = FOREASSOCIATIONS[value]

    class Info:
        value = "info"
        fore = FOREASSOCIATIONS[value]

    class Success:
        value = "success"
        fore = FOREASSOCIATIONS[value]
