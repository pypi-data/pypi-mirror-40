import json

from ..utils import open_stream
from . import defaults

__all__ = ["dump_json", "load_json"]


def dump_json(data, target=None, **settings):

    settings = settings or defaults.json_dump

    with open_stream(target, mode="w+", encoding="utf-8") as stream:
        data_dump = json.dumps(data, **settings)
        stream.write(data_dump)

    return data_dump


def load_json(source, **settings):

    settings = settings or defaults.json_load

    with open_stream(source, mode="r", encoding="utf-8") as stream:
        loaded_data = json.load(stream, **settings)

    return loaded_data
