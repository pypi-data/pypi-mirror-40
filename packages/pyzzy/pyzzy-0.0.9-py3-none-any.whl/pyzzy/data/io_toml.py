import toml

from ..utils import open_stream
from . import defaults

__all__ = ["dump_toml", "load_toml"]


def dump_toml(data, target=None, **settings):

    settings = settings or defaults.toml

    with open_stream(target, mode="w+", encoding="utf-8") as stream:
        data_dump = toml.dump(data, stream)

    return data_dump


def load_toml(source, **settings):

    settings = settings or defaults.toml

    with open_stream(source, mode="r", encoding="utf-8") as stream:
        loaded_data = toml.load(stream, **settings)

    return loaded_data
