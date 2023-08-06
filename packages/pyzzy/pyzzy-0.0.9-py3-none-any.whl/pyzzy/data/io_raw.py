from ..utils import open_stream

__all__ = ["dump_raw", "load_raw"]


def dump_raw(data, target, mode="w", encoding="utf-8", **kwargs):
    with open_stream(target, mode=mode, encoding=encoding) as stream:
        stream.write(data)


def load_raw(source, mode="r", encoding="utf-8"):
    with open_stream(source, mode=mode, encoding=encoding) as stream:
        return stream.read()
