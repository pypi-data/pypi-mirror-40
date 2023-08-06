from collections import namedtuple

import pytest

from pyzzy.utils.templates import render, traverse, attr, item


@pytest.fixture
def context_data():
    return {
        "__private": "invalid key",
        "public": "valid key",
        "node1": [
            "element_1",
            {
                "node2": [
                    "element_2",
                    "element_3",
                    {"node3": ["element_4", "element_5", "element_6"]},
                ]
            },
        ],
    }


@pytest.fixture
def tests_keys():
    return [
        "{{ __private }}",
        "{{ public }}",
        "{{ node1[1].node2[2].node3[-1] }}",
        "{{ node1/1/node2/2/node3/-1 }}",
    ]


def test_item_on_list():
    data = ["qux", "joe"]
    assert item(data, "1") == "joe"


def test_item_on_dict():
    data = {"foo": "qux", "bar": "joe"}
    assert item(data, "bar") == "joe"


def test_item_on_dict_return_none():
    data = {"foo": "qux", "bar": "joe"}
    assert item(data, "tux") is None


def test_attr_on_namedtuple():
    data = namedtuple("data", "foo, bar")("qux", "joe")
    assert attr(data, "bar") == "joe"


def test_attr_on_namedtuple_return_none():
    data = namedtuple("data", "foo, bar")("qux", "joe")
    assert attr(data, "tux") is None


def test_traverse_with_valid_key():
    data = {"key1": {"sub_key1": "value"}}
    assert traverse(data, "key1.sub_key1") == "value"


def test_traverse_with_invalid_key():
    data = {"key1": {"sub_key1": "value"}}
    assert traverse(data, 123) is None


def test_traverse_with_default():
    data = {"key1": {"sub_key1": "value"}}
    sentinel = ""
    assert traverse(data, "key1.missing_key", default=sentinel) is sentinel


def test_render_public_variable(context_data, tests_keys):
    # tests_keys[0] = "{{ __private }}"
    assert render(tests_keys[0], context_data) == "{{ __private }}"


def test_render_private_variable(context_data, tests_keys):
    # tests_keys[1] = "{{ public }}"
    assert render(tests_keys[1], context_data) == "valid key"


def test_render_mixed_key_path(context_data, tests_keys):
    # tests_keys[2] = "{{ node1[1].node2[2].node3[-1] }}"
    assert render(tests_keys[2], context_data) == "element_6"


def test_render_key_path_with_slashes(context_data, tests_keys):
    # tests_keys[3] = "{{ node1/1/node2/2/node3/-1 }}"
    assert render(tests_keys[3], context_data) == "element_6"
