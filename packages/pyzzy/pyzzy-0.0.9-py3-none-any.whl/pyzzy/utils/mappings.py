from argparse import Namespace
from collections import ChainMap
from collections.abc import Mapping, Sequence
from functools import reduce


class DeepChainMap(ChainMap):
    """Variant of ChainMap that allows direct updates to inner scopes"""

    def __setitem__(self, key, value):
        for mapping in self.maps:
            if key in mapping:
                mapping[key] = value
                break
        else:
            self.maps[0][key] = value

    def __delitem__(self, key):
        for mapping in self.maps:
            if key in mapping:
                del mapping[key]
                break
        else:
            raise KeyError(key)

    def merge(self):
        return merge_dicts(*self.maps[::-1])


def merge_dicts(*dicts):
    return reduce(lambda x, y: dict(_merge_2_dicts(x, y)), dicts[1:], dicts[0])


def _merge_2_dicts(dict1, dict2):
    keys = list(dict1)
    keys.extend(k for k in dict2 if k not in keys)
    for k in keys:
        if k in dict1 and k in dict2:
            if isinstance(dict1[k], dict) and isinstance(dict2[k], dict):
                yield (k, dict(_merge_2_dicts(dict1[k], dict2[k])))
            else:
                yield (k, dict2[k])
        elif k in dict1:
            yield (k, dict1[k])
        else:
            yield (k, dict2[k])


class AttrDict(dict):
    def __getattr__(self, name):
        if name in self:
            return self[name]
        else:
            raise AttributeError("No such attribute: " + name)

    def __setattr__(self, name, value):
        self[name] = value

    def __delattr__(self, name):
        if name in self:
            del self[name]
        else:
            raise AttributeError("No such attribute: " + name)

    def __dir__(self):
        return list(self.keys())


def ndict_cast(var, factory=Namespace):

    factories = {"attrdict": AttrDict, "namespace": Namespace}

    if not callable(factory):
        factory = factories.get(str(factory).lower(), Namespace)

    def cast(var):
        if isinstance(var, str):
            return var
        elif isinstance(var, Sequence):
            return type(var)(cast(item) for item in var)
        elif isinstance(var, Mapping):
            return factory(**{k: cast(var[k]) for k in var})
        else:
            return var

    return cast(var)
