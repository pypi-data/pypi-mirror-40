import os
import sys


PY36_PLUS = sys.version_info >= (3, 6)
fspath = str if not PY36_PLUS else os.fspath
