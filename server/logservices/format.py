from enum import Enum
from .level import LogLevel

class LogFormat(Enum):
    JSON = 1
    STANDART = 2
    LINUX_TERMINAL_LIKE = 3


class LogObject:
    def __init__(self, timestamp: str, context: str, level: LogLevel, message: str):
        self.timestamp = timestamp
        self.context = context
        self.level = level
        self.message = message

def format_log(log: LogObject, log_format: LogFormat, highlight=True):
    if log_format == LogFormat.JSON:
        return format_json(log, highlight)
    elif log_format == LogFormat.STANDART:
        return format_standart(log, highlight)
    elif log_format == LogFormat.LINUX_TERMINAL_LIKE:
        return format_linux_terminal_like(log, highlight)

def format_json(log: LogObject, highlight=True):
    if not highlight:
        msg = "{\n"
        msg += "    \"timestamp\": \"%s\",\n" % log.timestamp
        msg += "    \"context\": \"%s\",\n" % log.context
        msg += "    \"level\": \"%s\",\n" % log.level.value
        msg += "    \"message\": \"%s\"\n" % log.message
        msg += "}\n"
        return msg
    else:
        msg = "{\n"
        msg += "    \"timestamp\": \"%s\",\n" % log.timestamp
        msg += "    \"context\": \"%s\",\n" % log.context
        msg += "    \"level\": \"%s%s\033[0m\",\n" % (log.level.fore, log.level.value)
        msg += "    \"message\": \"%s\"\n" % log.message
        msg += "}\n"
        return msg
    
def format_linux_terminal_like(log: LogObject, highlight=True):
    if not highlight:
        return "%s@%s-[%s]:~$ %s\n" % (log.context, log.level.value, log.timestamp, log.message)
    else:
        return "%s%s@%s\033[0m-[%s]:~$ %s\n" % (log.level.fore, log.context, log.level.value, log.timestamp, log.message)

def format_standart(log: LogObject, highlight=True):
    if not highlight:
        return "[%s] [%s] [%s] %s\n" % (log.timestamp, log.context.upper(), log.level.value.upper(), log.message)
    else:
        return "[%s] [%s] [%s%s\033[0m] %s\n" % (log.timestamp, log.context.upper(), log.level.fore, log.level.value.upper(), log.message)