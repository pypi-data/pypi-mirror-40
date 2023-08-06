from ..compat import fspath

from .io_conf import dump_conf, load_conf
from .io_json import dump_json, load_json
from .io_raw import dump_raw, load_raw
from .io_toml import dump_toml, load_toml
from .io_yaml import dump_yaml, load_yaml


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
]

# Mapping that associate file extension to the appropriate dump function
dumpers = {
    "cfg": dump_conf,
    "conf": dump_conf,
    "ini": dump_conf,
    "json": dump_json,
    "toml": dump_toml,
    "yaml": dump_yaml,
    "yml": dump_yaml,
}

# Mapping that associate file extension to the appropriate load function
loaders = {
    "cfg": load_conf,
    "conf": load_conf,
    "ini": load_conf,
    "json": load_json,
    "toml": load_toml,
    "yaml": load_yaml,
    "yml": load_yaml,
}


def dump(data, file_path, **settings):
    """Dumps data to the appropriate format based on the file extension

    Args:
        data: Python object to dump.
        file_path (str, PathLike): File path used to write serialized data.
        settings: Optional arguments used by the dump funtion.

    Returns:
        str: Serialized data
    """

    # Avoid errors with Path objects
    file_path = fspath(file_path)

    # Normalize the file extension
    file_ext = file_path.rsplit(".", 1)[-1].lower()

    # Get the appropriate dumper based on file extension
    dump_data = dumpers.get(file_ext, dump_raw)

    return dump_data(data, file_path, **settings)


def load(file_path, **settings):
    """Loads data from the appropriate format based on the file extension

    Args:
        file_path (str, PathLike): File path used to read serialized data.
        settings: Optional arguments used by the load funtion.

    Returns:
        str: Deserialized data
    """

    # Avoid errors with Path objects
    file_path = fspath(file_path)

    # Normalize the file extension
    file_ext = file_path.rsplit(".", 1)[-1].lower()

    # Get the appropriate loader based on file extension
    load_data = loaders.get(file_ext, load_raw)

    return load_data(file_path, **settings)
