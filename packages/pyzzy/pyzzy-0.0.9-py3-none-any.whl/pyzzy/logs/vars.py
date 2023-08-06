import colorama


colorama.init()


def _set_tag(text, color):
    """Create tags with colors and format like [LEVL]"""

    # Some levels have specific brackets color else gray color
    brackets_color = {
        "CRIT": "LIGHTRED_EX",
        "ERRO": "LIGHTRED_EX",
        "WARN": "LIGHTYELLOW_EX",
    }.get(text, "LIGHTBLACK_EX")

    return "{}{}{}".format(
        _fg_colorize("[", brackets_color),
        _fg_colorize(text, color),
        _fg_colorize("]", brackets_color),
    )


def _fg_colorize(text, color):
    """Wrap string with ANSI color codes"""

    return "{}{}{}".format(
        getattr(colorama.Fore, color, colorama.Fore.WHITE),
        text,
        colorama.Style.RESET_ALL,
    )


CRITICAL = 50  # Serious problem, program may be unable to continue running
ERROR = 40  # Serious problem, program not been able to perform some function
WARNING = 30  # Unexpected thing happened, program is still working as expected
FAILURE = 22  # Similar to WARNING but for checks or tests
SUCCESS = 21  # Similar to INFO but for checks or tests
INFO = 20  # Confirmation that things are working as expected
DEBUG = 10  # Detailed information for diagnosing problems


_colored_tags = {
    CRITICAL: _set_tag("CRIT", "LIGHTRED_EX"),
    ERROR: _set_tag("ERRO", "LIGHTRED_EX"),
    WARNING: _set_tag("WARN", "LIGHTYELLOW_EX"),
    FAILURE: _set_tag("FAIL", "LIGHTYELLOW_EX"),
    SUCCESS: _set_tag("PASS", "LIGHTGREEN_EX"),
    INFO: _set_tag("INFO", "LIGHTBLUE_EX"),
    DEBUG: _set_tag("DBUG", "LIGHTBLACK_EX"),
}

_tags = {
    CRITICAL: "[CRIT]",
    ERROR: "[ERRO]",
    WARNING: "[WARN]",
    FAILURE: "[FAIL]",
    SUCCESS: "[PASS]",
    INFO: "[INFO]",
    DEBUG: "[DBUG]",
}


DEFAULT_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "console": {
            "()": "pyzzy.logs.PzConsoleFormatter",
            "format": "%(levelname)s %(message)s",
            "colored": True,
            "tracebacks": False,
        },
        "console_warnings": {
            "()": "pyzzy.logs.PzWarningsFormatter",
            "format": "%(filename)s:%(lineno)d: %(message)s",
        },
        "file": {
            "format": (
                "%(asctime)s - %(levelname)-8s"
                " - %(name)-11.11s - %(module)11.11s:%(lineno)03d"
                " :: %(message)s"
            )
        },
        "file_warnings": {
            "()": "pyzzy.logs.PzWarningsFormatter",
            "format": (
                "%(asctime)s - %(levelname)-8s"
                " - %(name)-11.11s - %(module)11.11s:%(lineno)03d"
                " :: %(message)s"
            ),
        },
    },
    "handlers": {
        "console_development": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "console",
        },
        "console_production": {
            "class": "logging.StreamHandler",
            "level": "WARNING",
            "formatter": "console",
        },
        "console_warnings": {
            "class": "logging.StreamHandler",
            "level": "WARNING",
            "formatter": "console_warnings",
        },
        "file": {
            "()": "pyzzy.logs.PzFileHandler",
            "level": "DEBUG",
            "formatter": "file",
            "filename": "logs/%(script_name)s_%(date)s.log",
            "mode": "a",
            "encoding": "utf-8",
            "delay": True,
        },
        "tr_file": {
            "()": "pyzzy.logs.PzTimedRotatingFileHandler",
            "level": "DEBUG",
            "formatter": "file",
            "filename": "logs/%(script_name)s_tr.log",
            "when": "midnight",
            "interval": 1,
            "backupCount": 0,
            "encoding": "utf-8",
            "delay": True,
            "utc": False,
            "suffix": "%Y%m%d%H%M%S.log",
            "extMatch": "^\\d{8}([-_]?\\d{2,6})?(\\.\\w+)?$",
        },
        "tr_file_warnings": {
            "()": "pyzzy.logs.PzTimedRotatingFileHandler",
            "level": "WARNING",
            "formatter": "file_warnings",
            "filename": "logs/%(script_name)s_tr.log",
            "when": "midnight",
            "interval": 1,
            "backupCount": 0,
            "encoding": "utf-8",
            "delay": True,
            "utc": False,
            "suffix": "%Y%m%d%H%M%S.log",
            "extMatch": "^\\d{8}([-_]?\\d{2,6})?(\\.\\w+)?$",
        },
    },
    "loggers": {
        "development": {
            "propagate": False,
            "level": "DEBUG",
            "handlers": ["console_development", "file"],
        },
        "production": {
            "propagate": False,
            "level": "DEBUG",
            "handlers": ["console_production", "tr_file"],
        },
        "py.warnings": {
            "propagate": False,
            "level": "DEBUG",
            "handlers": ["console_warnings", "tr_file_warnings"],
        },
    },
    "root": {"level": "DEBUG", "handlers": ["console_production", "tr_file"]},
}
