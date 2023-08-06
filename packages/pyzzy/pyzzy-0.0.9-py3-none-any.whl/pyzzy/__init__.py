import warnings

# Allows access to main features from module top-level
from .data import (
    dump,
    dump_conf,
    dump_json,
    dump_raw,
    dump_toml,
    dump_yaml,
    load,
    load_conf,
    load_json,
    load_raw,
    load_toml,
    load_yaml,
)
from .logs import getLogger, init_logging
from .utils import set_working_directory


__author__ = "krakozaure"
__license__ = "MIT"
__version__ = "0.0.9"

__all__ = [
    "dump",
    "dump_conf",
    "dump_json",
    "dump_raw",
    "dump_toml",
    "dump_yaml",
    "load",
    "load_conf",
    "load_json",
    "load_raw",
    "load_toml",
    "load_yaml",
    "getLogger",
    "init_logging",
    "set_working_directory",
]


warnings.filterwarnings(
    "once", category=PendingDeprecationWarning, module="pyzzy"
)
