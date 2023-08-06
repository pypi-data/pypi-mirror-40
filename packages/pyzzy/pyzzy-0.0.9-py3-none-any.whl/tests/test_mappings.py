import pytest

from pyzzy.utils.mappings import DeepChainMap, merge_dicts
from pyzzy.utils.mappings import AttrDict, Namespace, ndict_cast


@pytest.fixture
def db_conf_production():
    return {"production": "./production.db"}


@pytest.fixture
def db_conf_development():
    return {"development": "./development.db"}


@pytest.fixture
def db_conf():
    return {"production": "./production.db", "development": "./development.db"}


def test_merge_dicts():
    dict1 = {
        "key1": "value1",
        "key2": 123,
        "sub_dict": {"key3": "value3", "key4": "value4"},
    }
    dict2 = {"key2": 456, "sub_dict": {"key3": "new_value3", "key5": "value5"}}
    expected = {
        "key1": "value1",
        "key2": 456,
        "sub_dict": {"key3": "new_value3", "key4": "value4", "key5": "value5"},
    }
    assert merge_dicts(dict1, dict2) == expected


def test_DeepChainMap(db_conf_production, db_conf_development, db_conf):
    assert DeepChainMap(db_conf_production, db_conf_development) == db_conf


def test_DeepChainMap_get(db_conf_production, db_conf_development):
    dcm = DeepChainMap(db_conf_production, db_conf_development)
    assert dcm["production"] == "./production.db"
    assert dcm["development"] == "./development.db"


def test_DeepChainMap_set(db_conf_production, db_conf_development):
    dcm = DeepChainMap(db_conf_production, db_conf_development)
    dcm["production"] = "./prod.db"
    dcm["development"] = "./dvpt.db"
    assert dcm == {"production": "./prod.db", "development": "./dvpt.db"}


def test_DeepChainMap_del(db_conf_production, db_conf_development):
    dcm = DeepChainMap(db_conf_production, db_conf_development)
    del dcm["production"]
    del dcm["development"]
    assert dcm == {}


def test_DeepChainMap_merge(db_conf_production, db_conf_development, db_conf):
    dicts = db_conf_production, db_conf_development
    assert DeepChainMap(*dicts).merge() == db_conf


def test_DeepChainMap_set_new_key(db_conf_production, db_conf_development):
    dcm = DeepChainMap(db_conf_production, db_conf_development)
    dcm["tests"] = "./tests.db"
    expected = {
        "production": "./production.db",
        "development": "./development.db",
        "tests": "./tests.db",
    }
    assert dcm == expected


def test_DeepChainMap_del_raises(db_conf_production, db_conf_development):
    dcm = DeepChainMap(db_conf_production, db_conf_development)
    with pytest.raises(KeyError):
        del dcm["missing_key"]


def test_attrdict_get():
    data = AttrDict(key1="value1")
    assert data.key1 == "value1"


def test_attrdict_set():
    data = AttrDict(key1="value1")
    data.key1 = "new_value1"
    data.key2 = "value2"
    assert data["key1"] == "new_value1"
    assert data["key2"] == "value2"


def test_attrdict_del():
    data = AttrDict(key1="value1")
    del data.key1
    assert data == {}


def test_attrdict_get_raises():
    data = AttrDict()
    with pytest.raises(AttributeError):
        print(data.missing_key)


def test_attrdict_del_raises():
    data = AttrDict()
    with pytest.raises(AttributeError):
        del data.missing_key


def test_attrdict_dir():
    data = AttrDict(key1="value1", key2="value2")
    assert sorted(dir(data)) == ["key1", "key2"]


def test_ndict_cast_attrdict():
    data = {
        "key1": "value1",
        "key2": 123,
        "sub_dict": {"key3": "value3", "key4": ["a", "b", "c"]},
    }
    expected = AttrDict(
        key1="value1",
        key2=123,
        sub_dict=AttrDict(key3="value3", key4=["a", "b", "c"]),
    )
    assert ndict_cast(data, factory="attrdict") == expected


def test_ndict_cast_namespace():
    data = {
        "key1": "value1",
        "key2": 123,
        "sub_dict": {"key3": "value3", "key4": ["a", "b", "c"]},
    }
    expected = Namespace(
        key1="value1",
        key2=123,
        sub_dict=Namespace(key3="value3", key4=["a", "b", "c"]),
    )
    assert ndict_cast(data, factory="namespace") == expected
