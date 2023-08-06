import collections
import os
import sys

import pytest

import pyzzy as pz


os.chdir(os.path.dirname(__file__))

data_directory = os.path.join(os.getcwd(), "data")
if not os.path.isdir(data_directory):
    os.mkdir(data_directory)


@pytest.fixture
def DATA_SOURCE(factory=None):
    dict_factory = factory or collections.OrderedDict

    specials = dict_factory(
        (("deja-vu", "déjà vu"), ("multiline", "line1\nline2\nline3"))
    )
    numbers = dict_factory(
        (("one", 1), ("two", 2), ("three", 3), ("four", 4), ("five", 5))
    )
    data = dict_factory((("specials", specials), ("numbers", numbers)))
    return data


def serialize(var, indent=0):

    items = var.items() if isinstance(var, collections.abc.Mapping) else var

    # Python < 3.6 doesn't preserve order so at least,
    # sort the pairs to allow check on value
    if sys.version_info < (3, 6) and isinstance(var, collections.abc.Mapping):
        items = sorted(items, key=lambda item: item[0])

    key_len = max(len(("%s:" % k)) for k, v in items)
    prefix = " " * 4
    frmt = "\n%s%s %s"

    lines = ""
    for key, value in items:
        key = ("%s:" % key).ljust(key_len)
        if isinstance(value, (collections.abc.Mapping, list, tuple)):
            value = "\n%s%s" % (prefix, serialize(value, indent + 1))
        lines += frmt % (prefix * indent, key, value)

    return lines.strip()


def test_conf_object(DATA_SOURCE):
    data_tmp = pz.dump_conf(DATA_SOURCE)
    data_dst = pz.load_conf(data_tmp)
    data_dst = pz.data.io_conf.conf2dict(data_dst, include_default=False)
    assert serialize(DATA_SOURCE) == serialize(data_dst)


def test_conf_file(DATA_SOURCE):
    file_path = "data/data.conf"
    pz.dump_conf(DATA_SOURCE, file_path)
    data_dst = pz.load_conf(file_path)
    data_dst = pz.data.io_conf.conf2dict(data_dst, include_default=False)
    assert serialize(DATA_SOURCE) == serialize(data_dst)


def test_json_object(DATA_SOURCE):
    data_tmp = pz.dump_json(DATA_SOURCE)
    data_dst = pz.load_json(data_tmp)
    assert serialize(DATA_SOURCE) == serialize(data_dst)


def test_json_file(DATA_SOURCE):
    file_path = "data/data.json"
    pz.dump_json(DATA_SOURCE, file_path)
    data_dst = pz.load_json(file_path)
    assert serialize(DATA_SOURCE) == serialize(data_dst)


def test_toml_object(DATA_SOURCE):
    data_tmp = pz.dump_toml(DATA_SOURCE)
    data_dst = pz.load_toml(data_tmp)
    assert serialize(DATA_SOURCE) == serialize(data_dst)


def test_toml_file(DATA_SOURCE):
    file_path = "data/data.toml"
    pz.dump_toml(DATA_SOURCE, file_path)
    data_dst = pz.load_toml(file_path)
    assert serialize(DATA_SOURCE) == serialize(data_dst)


def test_yaml_object(DATA_SOURCE):
    data_tmp = pz.dump_yaml(DATA_SOURCE)
    data_dst = pz.load_yaml(data_tmp)
    assert serialize(DATA_SOURCE) == serialize(data_dst)


def test_yaml_file(DATA_SOURCE):
    file_path = "data/data.yaml"
    pz.dump_yaml(DATA_SOURCE, file_path)
    data_dst = pz.load_yaml(file_path)
    assert serialize(DATA_SOURCE) == serialize(data_dst)


def test_raw_file(DATA_SOURCE):
    file_path = "data/data.txt"
    DATA_SOURCE = str(DATA_SOURCE)
    pz.dump_raw(DATA_SOURCE, file_path)
    data_dst = pz.load_raw(file_path)
    assert DATA_SOURCE == data_dst


def test_default_dumper_loader(DATA_SOURCE):
    file_path = "data/data.txt"
    DATA_SOURCE = str(DATA_SOURCE)
    pz.dump(DATA_SOURCE, file_path)
    data_dst = pz.load(file_path)
    assert DATA_SOURCE == data_dst
