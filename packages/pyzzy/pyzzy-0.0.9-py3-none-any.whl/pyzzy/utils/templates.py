import re
from collections.abc import Sequence
from operator import getitem


RX_VAR = r"""
\{\{\s*
    (
        \w+
        (
            ([\.\-\/\[])?
            -?\w+
            (\])?
        )*
    )
\s*\}\}
"""
CRX_VAR = re.compile(RX_VAR, re.X | re.UNICODE)
CRX_KEY = re.compile(r"[\w\-]+", re.UNICODE)


def render(string, datas, default=None, crx_idpattern=CRX_VAR):
    def repl(sre_match, default=default):
        if default is None:
            default = sre_match.group(0)
        res = traverse(datas, sre_match.group(1), default=default)
        return str(res)

    return crx_idpattern.sub(repl, string)


def traverse(obj, key, default=None):

    if not isinstance(key, str):
        return default

    keys_list = CRX_KEY.findall(key)
    result = obj

    for key in keys_list:

        # Avoid private-like key access
        if key.startswith("__"):
            return default

        result = get_value(result, key, default)

        # Key is not found
        if result is default:
            return default

    return result


def get_value(obj, key, default=None):
    return item(obj, key) or attr(obj, key) or default


def item(obj, name):
    try:
        if isinstance(obj, Sequence):
            name = int(name)
        return getitem(obj, name)
    except (IndexError, KeyError, TypeError, ValueError):
        return None


def attr(obj, name):
    try:
        return getattr(obj, name)
    except (AttributeError, TypeError):
        return None
