import contextlib
import io
import json
import logging
import os
import re
import time
import warnings

import pyzzy as pz


os.chdir(os.path.dirname(__file__))

pz.init_logging(
    config=pz.logs.DEFAULT_CONFIG,
    capture_warnings=True,
    simple_warnings=True,
    raise_exceptions=True,  # no error swallowing (tests=development mode)
)


@contextlib.contextmanager
def capture_handler_stream(logger, handler_name):
    handler = get_handler_by_name(logger.handlers, handler_name)
    old_stream = handler.stream
    new_stream = io.StringIO()
    handler.stream = new_stream
    try:
        yield new_stream
    finally:
        new_stream.close()
        handler.stream = old_stream


def get_handler_by_name(handlers, name):
    for handler in handlers:
        if handler.get_name() == name:
            return handler


def test_get_config_from_None():
    assert pz.logs._get_config(config=None) == pz.logs.DEFAULT_CONFIG


def test_get_config_from_file():
    config_file = "configurations/logging.json"
    with open(config_file) as f:
        expected_config = json.load(f)
    assert pz.logs._get_config(config=config_file) == expected_config


def test_root_handlers_names():
    import _pytest.logging

    logger = logging.getLogger()
    handlers_names = [handler.get_name() for handler in logger.handlers]
    expected_names = {"console_production", "tr_file"}
    assert expected_names.issubset(handlers_names)


def test_root_console_handler_output():
    logger = logging.getLogger()
    message = "Log message"

    with capture_handler_stream(logger, "console_production") as stream:
        logger.error(message)
        logger.debug(message)
        captured_output = stream.getvalue()

    assert message in captured_output
    assert pz.logs.vars._colored_tags[logging.ERROR] in captured_output
    assert pz.logs.vars._colored_tags[logging.DEBUG] not in captured_output


def test_root_console_handler_output_without_traceback():
    logger = logging.getLogger()
    message = "Zero division error !"

    with capture_handler_stream(logger, "console_production") as stream:
        try:
            print("1 / 0 =", 1 / 0)
        except ZeroDivisionError:
            logger.exception(message)
        captured_output = stream.getvalue()

    assert "ZeroDivisionError" not in captured_output
    assert message in captured_output
    assert pz.logs.vars._colored_tags[logging.ERROR] in captured_output


def test_root_trfile_handler_output():
    logger = logging.getLogger()
    message = "Log message"

    with capture_handler_stream(logger, "tr_file") as stream:
        logger.error(message)
        logger.debug(message)
        captured_output = stream.getvalue()

    assert message in captured_output
    assert logging._levelToName[logging.ERROR] in captured_output
    assert logging._levelToName[logging.DEBUG] in captured_output
    assert time.strftime("%Y-%m-%d %H:%M") in captured_output
    assert logger.name in captured_output


def test_warnings_console_formatter():
    logger = logging.getLogger("py.warnings")
    message = "Warning message !"

    with capture_handler_stream(logger, "console_warnings") as stream:
        warnings.warn(message)
        logger.warning(message)
        captured_output = stream.getvalue()

    warning_re = "(?P<file>.+?):(?P<line>\d+?): (?P<message>.+)"
    warning_cre = re.compile(warning_re)
    sre_matches = [match for match in warning_cre.finditer(captured_output)]

    assert len(sre_matches) == 2
    assert sre_matches[0].group("file") in __file__
    assert sre_matches[0].group("message") == "UserWarning: Warning message !"


def test_success_and_failure_logger_methods():
    logger = logging.getLogger("development")
    message = "Log message"

    with capture_handler_stream(logger, "console_development") as stream:
        logger.failure(message)
        logger.success(message)
        captured_output = stream.getvalue()

    failure_level = logging._nameToLevel["FAILURE"]
    success_level = logging._nameToLevel["SUCCESS"]

    assert message in captured_output
    assert pz.logs.vars._colored_tags[failure_level] in captured_output
    assert pz.logs.vars._colored_tags[success_level] in captured_output
