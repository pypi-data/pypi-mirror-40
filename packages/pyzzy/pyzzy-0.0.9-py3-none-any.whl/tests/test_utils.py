import os
import pathlib

import pytest

from pyzzy.utils import (
    fspath,
    is_dir,
    is_file,
    search_files,
    set_working_directory,
)


@pytest.fixture
def temp_dir(tmpdir):
    """Create temporary directory tree structure used for the tests

    <temp_dir>
    |-- src/
    |   |-- __init__.py
    |   |-- core.py
    |   |-- utils.py
    |-- LICENSE
    |-- README.md
    |-- setup.py
    """

    files_list = [
        "src/__init__.py",
        "src/core.py",
        "src/utils.py",
        "LICENSE",
        "README.md",
        "setup.py",
    ]
    temp_dir_ = str(tmpdir.mkdtemp())
    for file_path in files_list:
        p = pathlib.Path(temp_dir_) / file_path
        if not p.parent.exists():
            os.makedirs(str(p.parent), exist_ok=True)
        p.touch()
    return temp_dir_


def test_fspath():
    assert fspath(pathlib.Path(".")) == "."


def test_is_file_return_true():
    assert is_file(__file__) is True


def test_is_file_return_false():
    assert is_file({}) is False


def test_is_dir_return_true():
    directory = os.path.dirname(os.path.abspath(__file__))
    assert is_dir(directory) is True


def test_is_dir_return_false():
    assert is_dir({}) is False


def test_search_files_without_parameters(temp_dir):
    results = search_files(temp_dir)
    expected = [
        temp_dir + "/LICENSE",
        temp_dir + "/README.md",
        temp_dir + "/setup.py",
    ]

    results = sorted(results)
    expected = sorted(pathlib.Path(p) for p in expected)

    assert results == expected


def test_search_files_with_parameters(temp_dir):
    parameters = {"patterns": "*.py", "recursive": True}

    results = search_files(temp_dir, **parameters)
    expected = [
        temp_dir + "/setup.py",
        temp_dir + "/src/__init__.py",
        temp_dir + "/src/core.py",
        temp_dir + "/src/utils.py",
    ]

    results = sorted(results)
    expected = sorted(pathlib.Path(p) for p in expected)

    assert results == expected


def test_set_working_dir():
    expected = os.path.dirname(os.path.abspath(__file__))
    result = set_working_directory(__file__)
    assert result == expected
