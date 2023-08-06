import pytest

from pyzzy.utils import nested


@pytest.fixture
def DATA_SOURCE():
    return {"key1": [{"key2": [{"key3": "value1"}]}]}


def test_proxybase_dunders():
    data = {"key1": "value1", "key2": "value2"}
    pb = nested.ProxyBase(data)
    assert pb
    assert dir(pb) == dir(data)
    assert sorted(k for k in pb) == sorted(k for k in data)
    assert len(pb) == len(data)
    assert repr(pb) == repr(data)
    assert str(pb) == str(data)


def test_unset():
    assert repr(nested.UNSET) == "<UNSET>"


def test_resolve_key_path_with_invalid_keys_paths():
    assert nested.resolve_key_path({}, "") == ({}, "")
    assert nested.resolve_key_path({}, None) == ({}, None)


def test_resolve_key_path_with_simple_key_path(DATA_SOURCE):
    assert nested.resolve_key_path(DATA_SOURCE, "key1") == (DATA_SOURCE, "key1")


def test_split_key_path_raises_valueerror():
    with pytest.raises(ValueError):
        nested._split_key_path("")

    with pytest.raises(ValueError):
        nested._split_key_path(".")

    with pytest.raises(ValueError):
        nested._split_key_path("[]")


def test_split_keys_with_simple_key_path():
    assert nested._split_keys("key") == ["key"]


def test_nproxy_nget(DATA_SOURCE):
    expected = DATA_SOURCE["key1"][0]["key2"][-1]["key3"]
    assert nested.NProxy(DATA_SOURCE).nget("key1[0].key2[-1].key3") == expected


def test_nproxy_nget_raises():
    with pytest.raises(nested.NestedOperationError):
        nested.NProxy().nget("key1[0].key2[-1].key3", default=nested.UNSET)


def test_nproxy_nget_default():
    assert nested.NProxy().nget("key1[0].key2[-1].key3") is None


def test_nproxy_getitem(DATA_SOURCE):
    expected = DATA_SOURCE["key1"][0]["key2"][-1]["key3"]
    assert nested.NProxy(DATA_SOURCE)["key1[0].key2[-1].key3"] == expected


def test_nproxy_getitem_raises():
    with pytest.raises(nested.NestedOperationError):
        print(nested.NProxy()["key1[0].key2[-1].key3"])


def test_nproxy_nset(DATA_SOURCE):
    proxy = nested.NProxy(DATA_SOURCE)
    expected = "value2 (created)"
    proxy.nset("key1[0].key2[-1].key4", expected)
    assert proxy["key1"][0]["key2"][-1]["key4"] == expected


def test_nproxy_nset_raises():
    with pytest.raises(nested.NestedOperationError):
        nested.NProxy().nset("key1[0].key2[-1].key3", "value")


def test_nproxy_setitem(DATA_SOURCE):
    proxy = nested.NProxy(DATA_SOURCE)
    expected = "value2 (created)"
    proxy["key1[0].key2[-1].key4"] = expected
    assert proxy["key1"][0]["key2"][-1]["key4"] == expected


def test_nproxy_setitem_raises():
    with pytest.raises(nested.NestedOperationError):
        nested.NProxy()["key1[0].key2[-1].key3"] = "value"


def test_nproxy_ndel(DATA_SOURCE):
    proxy = nested.NProxy(DATA_SOURCE)
    proxy.ndel("key1[0].key2[-1].key3")
    assert proxy["key1"][0]["key2"][-1] == {}


def test_nproxy_ndel_raises():
    with pytest.raises(nested.NestedOperationError):
        nested.NProxy().ndel("key1[0].key2[-1].key3")


def test_nproxy_delitem(DATA_SOURCE):
    proxy = nested.NProxy(DATA_SOURCE)
    del proxy["key1[0].key2[-1].key3"]
    assert proxy["key1"][0]["key2"][-1] == {}


def test_nproxy_delitem_raises():
    with pytest.raises(nested.NestedOperationError):
        del nested.NProxy()["key1[0].key2[-1].key3"]


def test_nproxy_ncopy(DATA_SOURCE):
    assert nested.NProxy(DATA_SOURCE).ncopy() == DATA_SOURCE


def test_ncontains(DATA_SOURCE):
    proxy = nested.NProxy(DATA_SOURCE)
    assert ("key1[0].key2[-1].key3" in proxy) is True


def test_ncontains_return_false(DATA_SOURCE):
    proxy = nested.NProxy(DATA_SOURCE)
    assert ("key1[0].key2[-1].missing_key" in proxy) is False
