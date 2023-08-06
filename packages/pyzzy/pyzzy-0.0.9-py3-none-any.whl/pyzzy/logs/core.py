import datetime
import inspect
import logging
import os
import os.path
import re
import sys

from ..compat import fspath
from ..utils import ensure_dir_exists
from ..utils import get_path_infos
from .vars import _colored_tags
from .vars import _tags
from .vars import FAILURE
from .vars import SUCCESS


class PzConsoleFormatter(logging.Formatter):
    """Formatter with optionals colors and traceback"""

    def __init__(self, fmt=None, datefmt=None, style="%",
                 colored=True, tracebacks=False):
        super().__init__(fmt=fmt, datefmt=datefmt, style=style)
        self.used_tags = _colored_tags if colored else _tags
        self.tracebacks = tracebacks

    def format(self, record):

        # Avoid corrupting original record if another handler is used next
        record = logging.makeLogRecord(vars(record))

        # Shortens the level name (add colors if required)
        record.levelname = self.used_tags[record.levelno]

        # Avoid duplicated traceback on console
        if record.exc_info and not self.tracebacks:
            record.exc_info = None

        return super().format(record)


class PzWarningsFormatter(logging.Formatter):
    """Formatter with correct warning values"""

    def format(self, record):
        record = self.update_record_from_warning(record)
        return super().format(record)

    def update_record_from_warning(self, record):
        """Update the record with correct filename, lineno and module values"""

        # Avoid corrupting original record if another handler is used next
        record = logging.makeLogRecord(vars(record))

        # Find the frame corresponding to warnings._showwarnmsg
        caller_infos = record.pathname, record.lineno, record.funcName
        frame = _find_warning_caller(*caller_infos)

        if not frame or "msg" not in frame.f_locals:
            return record

        msg = frame.f_locals["msg"]

        record.filename = getattr(msg, "filename", record.filename)
        record.lineno = getattr(msg, "lineno", record.lineno)
        record.message = getattr(msg, "message", record.msg)

        record.filename = os.path.basename(record.filename)
        record.module = os.path.splitext(record.filename)[0]
        record.message = str(record.message)

        return record


class PzFileHandler(logging.FileHandler):
    """FileHandler with dynamic log path creation"""

    def __init__(self, filename, mode="a", encoding="utf-8", delay=False):
        filename = _set_log_path(filename)
        super().__init__(filename, mode, encoding, delay)

    def _open(self):
        log_dir = os.path.dirname(os.path.abspath(self.baseFilename))
        ensure_dir_exists(log_dir, mode=0o600)
        return open(self.baseFilename, self.mode, encoding=self.encoding)


class PzTimedRotatingFileHandler(logging.handlers.TimedRotatingFileHandler):
    """TimedRotatingFileHandler with dynamic log path creation"""

    def __init__(self, filename, when="midnight", interval=1, backupCount=0,
                 encoding="utf-8", delay=True, utc=False,
                 suffix=None, extMatch=None, atTime=None):

        filename = _set_log_path(filename)
        super().__init__(
            filename, when, interval, backupCount, encoding, delay, utc, atTime
        )

        # Allow user to set how time-rotating filename suffix looks like
        if isinstance(suffix, str) and isinstance(extMatch, str):
            self.suffix = suffix
            self.extMatch = re.compile(extMatch)

    def _open(self):
        log_dir = os.path.dirname(os.path.abspath(self.baseFilename))
        ensure_dir_exists(log_dir, mode=0o600)
        return open(self.baseFilename, self.mode, encoding=self.encoding)


class PzLogger(logging.getLoggerClass()):
    """Subclass from Logger to add custom logging level methods"""

    def failure(self, msg, *args, **kwargs):
        if self.isEnabledFor(FAILURE):
            self._log(FAILURE, msg, args, **kwargs)

    def success(self, msg, *args, **kwargs):
        if self.isEnabledFor(SUCCESS):
            self._log(SUCCESS, msg, args, **kwargs)


def _find_warning_caller(filename, lineno, function):
    # FrameInfo(frame, filename, lineno, function, code_context, index)
    for frame_info in inspect.stack():
        if frame_info[1:4] == (filename, lineno, function):
            return frame_info[0]


def _set_log_path(log_path):

    log_path = fspath(log_path)

    if "%(script_name)s" in log_path:
        script_file = _get_default_log_path()
        script_name = get_path_infos(script_file).stem
        log_path = log_path.replace("%(script_name)s", script_name)

    if "%(date)s" in log_path:
        date = datetime.datetime.now().strftime("%Y%m%d")
        log_path = log_path.replace("%(date)s", date)

    return log_path


def _get_default_log_path():
    """Define default logger's file path relative to main script directory
       rather than current working directory
    """

    # Extract main script path directory and filename (without extension)
    # Main script directory is preferable over current working directory
    script = sys.modules["__main__"].__file__

    script_infos = get_path_infos(script)
    script_dir, script_name = script_infos.parent, script_infos.stem

    # Avoid modifying python install directory
    if script_dir.lower().startswith(sys.exec_prefix.lower()):
        script_dir = os.getcwd()
        script_name = __package__.split(".")[0]

    return os.path.join(script_dir, "logs", script_name + ".log")


# Register the new logger and add custom logging levels
logging.setLoggerClass(PzLogger)
logging.addLevelName(FAILURE, "FAILURE")
logging.addLevelName(SUCCESS, "SUCCESS")
