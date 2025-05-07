import inspect
import os, sys 
import traceback
from typing import Dict, Callable, Tuple

import logging
import copy

class ColorFormatter(logging.Formatter):
    """Formatter with support for colored log messages."""
    COLORS = {
        "DEBUG": "\033[36m",     # Cyan
        "INFO": "\033[32m",      # Green
        "WARNING": "\033[33m",   # Yellow 
        "ERROR": "\033[31m",     # Red
        "CRITICAL": "\033[35m",  # Purple
        "RESET": "\033[0m",
    }

    def format(self, record):
        record_copy = copy.copy(record)
        color = self.COLORS.get(record_copy.levelname, "")
        reset = self.COLORS["RESET"]
        record_copy.levelname = f"{color}{record_copy.levelname}{reset}"
        record_copy.msg = f"{color}{record_copy.msg}{reset}"
        if hasattr(record_copy, 'caller_filename'):
            record_copy.caller_filename = f"{color}{record_copy.caller_filename}{reset}"
        if hasattr(record_copy, 'caller_func'):
            record_copy.caller_func = f"{color}{record_copy.caller_func}{reset}"
        if hasattr(record_copy, 'caller_line'):
            record_copy.caller_line = f"{color}{record_copy.caller_line}{reset}"
        return super().format(record_copy)
    
class BaseFormatter(logging.Formatter):
    """Basic formatter without color support"""
    def format(self, record):
        return super().format(record)

class Logger:
    def __init__(self, log_path: str = "") -> None:
        # Create logger
        self.logger = logging.getLogger("sync_logger")
        self.logger.setLevel(logging.DEBUG)

        for handler in self.logger.handlers[:]:
            handler.close()  # Close the handler (important for file handlers)
            self.logger.removeHandler(handler)
        
        # Create handlers
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(ColorFormatter(
            fmt="%(asctime)s - %(levelname)s - [%(caller_filename)s:%(caller_func)s:%(caller_line)s] - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        ))
        self.logger.addHandler(console_handler)

        if log_path:
            # Create directory if needed
            os.makedirs(os.path.dirname(log_path), exist_ok=True)
            
            # Add file handler
            file_handler = logging.FileHandler(log_path)
            file_handler.setFormatter(BaseFormatter(
                fmt="%(asctime)s - %(levelname)s - [%(caller_filename)s:%(caller_func)s:%(caller_line)s] - %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S"
            ))
            self.logger.addHandler(file_handler)

    def _log(self, level: str, message: str):
        # Get caller information
        caller = inspect.currentframe().f_back.f_back  # Go back two frames to get the actual caller
        caller_filename = caller.f_code.co_filename
        func_name = caller.f_code.co_name
        line_no = caller.f_lineno
        
        # Add caller information to extra
        extra = {
            'caller_filename': caller_filename,
            'caller_func': func_name,
            'caller_line': line_no
        }
        
        # Log with extra information
        self.logger.log(getattr(logging, level), message, extra=extra)

    def debug(self, message: str):
        self._log('DEBUG', message)

    def info(self, message: str):
        self._log('INFO', message)

    def warning(self, message: str):
        self._log('WARNING', message)

    def error(self, message: str):
        self._log('ERROR', message)

    def critical(self, message: str):
        self._log('CRITICAL', message)

    def critical(self, message: str):
        self._log('CRITICAL', message)
        if isinstance(message, Exception):
            stack_trace = "".join(traceback.format_exception(type(message), message, message.__traceback__))
            self._log('CRITICAL', f"Exception Stack Trace:\n{stack_trace}")
        else:
            # Get the stack trace but skip the last two frames (current function and _log)
            stack_frames = traceback.extract_stack()[:-2]
            formatted_trace = []
            for filename, lineno, name, line in stack_frames:
                if name != '<module>':  # Skip module level calls
                    formatted_trace.append(f'  File "{filename}", line {lineno}, in {name}\n    {line}\n')
            if formatted_trace:
                self._log('CRITICAL', "Stack Trace:\n" + "".join(formatted_trace))

    def __del__(self):
        """Cleanup when logger is destroyed"""
        for handler in self.logger.handlers[:]:
            handler.close()
            self.logger.removeHandler(handler)

class LoggerManager:
    _instances: Dict[str, Logger] = {}

    @classmethod
    def get_logger(cls, log_path: str = "") -> Logger:
        if log_path not in cls._instances:
            cls._instances[log_path] = Logger(log_path)
        return cls._instances[log_path]

def _log_assert(cond: bool, msg: str = "", e: Exception = None, force_quit=True):
    if not cond:
        logger = LoggerManager.get_logger()
        logger.error(msg)
        if e:
            logger.error("".join(traceback.format_exception(type(e), e, e.__traceback__)))
        else:
            logger.error("".join(traceback.format_stack()))
        if force_quit:
            sys.exit(-1)
        else:
            raise

def init_logger(log_path: str = "/tmp/app.log") -> Tuple[Callable, ...]:
    """Initialize logger with specified path"""
    logger = LoggerManager.get_logger(log_path)

    logd = logger.debug
    logi = logger.info
    logw = logger.warning
    loge = logger.error
    logf = logger.critical
    log_assert = _log_assert

    return logd, logi, logw, loge, logf, log_assert


# project root path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

# # 如果log文件夹不存在，创建
# if not os.path.exists(f"{project_root}/log"):
#     os.makedirs(f"{project_root}/log")

# Global logger instance
logger = LoggerManager.get_logger(f"{project_root}/log/app.log")
logi = logger.info
logd = logger.debug
logw = logger.warning
loge = logger.error
logf = logger.critical
log_assert = _log_assert