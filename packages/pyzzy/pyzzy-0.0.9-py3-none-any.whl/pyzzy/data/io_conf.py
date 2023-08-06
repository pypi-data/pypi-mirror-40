import collections
import configparser

from ..utils import open_stream, identity
from . import defaults


__all__ = ["dump_conf", "load_conf", "conf2dict"]


def dump_conf(data, target=None, **settings):

    settings = settings or defaults.conf
    parser = _conf_factory(settings)

    with open_stream(target, mode="w+", encoding="utf-8") as stream:
        parser.read_dict(data)
        parser.write(stream)
        stream.seek(0)
        data_dump = stream.read()

    return data_dump


def load_conf(source, **settings):

    settings = settings or defaults.conf
    parser = _conf_factory(settings)

    with open_stream(source, mode="r", encoding="utf-8") as stream:
        parser.read_file(stream)

    return parser


def conf2dict(conf, include_default=True, factory=None):

    factory = factory or collections.OrderedDict
    conf_dict = factory()

    for section_name in conf:

        if section_name == conf.default_section and not include_default:
            continue

        section = conf[section_name]
        conf_dict[section_name] = factory(
            (key, section.get(key, raw=False))
            for key in section
            if key not in conf.defaults()
        )

    return conf_dict


def _conf_factory(settings):

    # By default, each option name are converted in lowercase by python
    # If no optionxform is given, identity avoid option name modifications
    optionxform = settings.pop("optionxform", identity)
    optionxform = optionxform if callable(optionxform) else identity

    parser = configparser.ConfigParser(**settings)
    parser.optionxform = optionxform

    return parser
