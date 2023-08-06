from logging import getLogger
import logging
import logging.config
import warnings

# Allows imports from pyzzy.logs.XXXX (useful for configuration files)
from .core import PzConsoleFormatter
from .core import PzFileHandler
from .core import PzTimedRotatingFileHandler
from .core import PzWarningsFormatter

# Logging configuration handling
from ..data import load
from ..utils import is_file
from .vars import DEFAULT_CONFIG


__all__ = [
    "getLogger",
    "init_logging",
    "PzConsoleFormatter",
    "PzFileHandler",
    "PzTimedRotatingFileHandler",
    "PzWarningsFormatter",
]


def init_logging(config=None, capture_warnings=True, simple_warnings=True,
                 raise_exceptions=False):
    """Load logging configuration from user or default configuration

    Parameters
    ----------
    config (None, PathLike, dict, False) :
        Whole configuration to load for the logging module
        If config is None, DEFAULT_CONFIG will be loaded
        If config is a path, it can be loaded from files handled by pyzzy.data
        If config is False-like, no configuration is loaded
    capture_warnings (bool) :
        Capture (or not) the warnings and delegate to the 'py.warnings' logger
    simple_warnings (bool) :
        Simplify warning format to return message like 'Category: Message'
    raise_exceptions (bool) :
        Should be False in production, True for development
    """

    config = _get_config(config)

    if config:
        logging.config.dictConfig(config)

    logging.captureWarnings(capture_warnings)

    if simple_warnings:
        warnings.formatwarning = simple_warning_format

    logging.raiseExceptions = raise_exceptions


def _get_config(config):
    if config is None:
        return DEFAULT_CONFIG
    elif is_file(config):
        return load(config)
    else:
        return config


def simple_warning_format(message, category, *args, **kwargs):
    return "%s: %s" % (category.__name__, str(message))
