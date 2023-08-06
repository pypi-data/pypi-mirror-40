from copy import deepcopy
from itertools import chain as itertools_chain


class Unset:
    def __repr__(self):
        return "<UNSET>"


UNSET = Unset()


class NestedOperationError(Exception):
    pass


class ProxyBase(object):
    def __init__(self, data=None):
        self.data = data or {}

    def __bool__(self):
        return bool(self.data)

    def __dir__(self):
        return dir(self.data)

    def __iter__(self):
        return iter(self.data)

    def __len__(self):
        return len(self.data)

    def __repr__(self):
        return repr(self.data)

    def __str__(self):
        return str(self.data)


class NProxy(ProxyBase):
    def __getitem__(self, key):
        return nget(self.data, key, default=UNSET)

    def __setitem__(self, key, value):
        return nset(self.data, key, value)

    def __delitem__(self, key):
        ndel(self.data, key)

    def __contains__(self, key):
        return ncontains(self.data, key)

    def nget(self, key, default=None):
        return nget(self.data, key, default=default)

    def nset(self, key, value):
        return nset(self.data, key, value)

    def ndel(self, key):
        ndel(self.data, key)

    def ncopy(self):
        return deepcopy(self.data)


def nget(data, key, default=None):
    try:
        data, key = resolve_key_path(data, key)
        value = data[key]
    except (IndexError, KeyError, TypeError):
        if default is UNSET:
            raise NestedOperationError("Get operation failed")
        value = default() if callable(default) else default
    return value


def nset(data, key, value):
    try:
        data, key = resolve_key_path(data, key)
        data[key] = value
    except (IndexError, KeyError, TypeError):
        raise NestedOperationError("Set operation failed")
    return value


def ndel(data, key):
    try:
        data, key = resolve_key_path(data, key)
        del data[key]
    except (IndexError, KeyError, TypeError):
        raise NestedOperationError("Delete operation failed")


def ncontains(data, key):
    try:
        data, key = resolve_key_path(data, key)
        data[key]
        return True
    except (IndexError, KeyError, TypeError):
        return False


def resolve_key_path(data, key_path):

    if not key_path or not isinstance(key_path, (str, bytes)):
        return (data, key_path)

    first_keys, last_key = _split_key_path(key_path)

    if not first_keys:
        return (data, last_key)

    for key in first_keys:
        data = data[key]

    return (data, last_key)


def _split_key_path(key_path):
    if not key_path or not isinstance(key_path, (str, bytes)):
        raise ValueError("'key_path' must be a non-empty string")

    if "." in key_path:
        keys_list = _split_keys(key_path)
    else:
        keys_list = _split_indexes(key_path)

    keys_list = [k for k in keys_list if k != ""]
    if not keys_list:
        raise ValueError("invalid 'key_path'")

    return keys_list[:-1], keys_list[-1]


def _split_keys(key_path):
    if "." not in key_path:
        return [key_path]

    return itertools_chain(*(_split_indexes(k) for k in key_path.split(".")))


def _split_indexes(key_path):
    if "[" not in key_path:
        return [key_path]

    # key_path = "foo[0][0]" --> key = "foo", indexes=(0, 0)
    # key_path = "[0][0]"    --> key = "",    indexes=(0, 0)
    parts = key_path.split("[")
    key = parts[0]
    indexes = (int(k[:-1]) for k in parts[1:])
    return itertools_chain([key], indexes)
