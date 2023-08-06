import ruamel.yaml

from ..utils import open_stream
from . import defaults

__all__ = ["dump_yaml", "load_yaml"]


def dump_yaml(data, target=None, **settings):

    settings = settings or defaults.yaml
    yaml = _yaml_factory(settings)

    with open_stream(target, mode="w+", encoding="utf-8") as stream:
        yaml.dump(data, stream)
        stream.seek(0)
        data_dump = stream.read()

    return data_dump


def load_yaml(source, **settings):

    settings = settings or defaults.yaml
    yaml = _yaml_factory(settings)

    with open_stream(source, mode="r", encoding="utf-8") as stream:
        loaded_data = yaml.load(stream)

    return loaded_data


def _yaml_factory(settings, yml=None):

    if not yml:
        typ = settings.pop("typ", "rt").lower()
        typ = typ if typ in {"safe", "unsafe"} else "rt"
        yml = ruamel.yaml.YAML(typ=typ)

    for attr in defaults.yaml:
        setattr(yml, attr, defaults.yaml[attr])

    for attr in settings:
        setattr(yml, attr, settings[attr])

    return yml
