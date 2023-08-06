from collections.abc import Sequence
from fnmatch import fnmatch
import collections
import io
import os
import pathlib

from ..compat import fspath

from . import dispatchers
from . import mappings
from . import nested
from . import templates


def identity(var):
    return var


def open_stream(resource=None, mode="r", encoding="utf-8"):
    read_mode = "r" in mode
    as_file = is_file(resource)

    if (read_mode and as_file) or (not read_mode and resource):
        resource = fspath(resource)
        stream = open(resource, mode=mode, encoding=encoding)

    elif (read_mode and not as_file) or (not read_mode and not resource):
        stream = io.StringIO(resource or "")

    return stream


def set_working_directory(path):
    path = fspath(path)
    path = os.path.abspath(path)

    if is_file(path):
        path = os.path.dirname(path)

    os.chdir(path)
    return path


def get_path_infos(path):
    """Get  basic informations from a path"""

    path = fspath(path)
    path = os.path.abspath(path)
    path = pathlib.PurePath(path)

    return PathInfos(
        path.drive,
        str(path.parent),
        path.name,
        path.stem,
        path.suffix,
        os.path.sep,
    )


PathInfos = collections.namedtuple(
    "PathInfos", "drive parent name stem ext sep"
)


def ensure_dir_exists(path, mode=0o600):
    """If the directory does not already exist,
       create it and all intermediate-level directories
    """
    path = fspath(path)
    if not is_dir(path) and not is_file(path):
        os.makedirs(path, mode=mode)


def is_dir(path):
    try:
        path = fspath(path)
        return os.path.isdir(path)
    except TypeError:
        return False


def is_file(path):
    try:
        path = fspath(path)
        return os.path.isfile(path)
    except TypeError:
        return False


def search_files(directory, patterns=None, recursive=False):
    directory = pathlib.Path(directory)

    # any_fnmatch iterate on sequence of string
    if isinstance(patterns, str) or not isinstance(patterns, Sequence):
        patterns = (patterns,)
    patterns = tuple(p for p in set(patterns) if p and isinstance(p, str))

    # Search could be recursive
    glob_pattern = "**" if recursive else "."
    # Filename could be filtered wih 0, 1 or N patterns
    glob_pattern += "/*"

    # Scan directory and yield only required file paths
    for entry in directory.glob(glob_pattern):
        if entry.is_file() and any_fnmatch(entry.name, patterns):
            yield entry


def any_fnmatch(entry_name, patterns):
    # No patterns, so return all paths
    if not patterns:
        return True
    # Check if at least one pattern matches the entry name
    return any(fnmatch(entry_name, pattern) for pattern in patterns)
