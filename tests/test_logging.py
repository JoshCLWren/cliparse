"""Tests for cliparse.logging module."""

import logging

from cliparse.config import CliConfig
from cliparse.logging import LoggingContext, configure_logging, get_logger


def test_configure_logging_default():
    """Test configure_logging with default config."""
    config = CliConfig()
    logger = configure_logging(config)

    assert logger is not None
    assert logger.level == logging.INFO


def test_configure_logging_verbose():
    """Test configure_logging with verbose config."""
    config = CliConfig(verbose=1)
    logger = configure_logging(config)

    assert logger.level == logging.INFO


def test_configure_logging_very_verbose():
    """Test configure_logging with very verbose config."""
    config = CliConfig(verbose=2)
    logger = configure_logging(config)

    assert logger.level == logging.DEBUG


def test_configure_logging_quiet():
    """Test configure_logging with quiet config."""
    config = CliConfig(quiet=True)
    logger = configure_logging(config)

    assert logger.level == logging.WARNING


def test_configure_logging_with_log_file(tmp_path):
    """Test configure_logging with log file."""
    log_file = tmp_path / "test.log"
    config = CliConfig(log_file=str(log_file))
    logger = configure_logging(config)

    assert logger is not None
    assert log_file.exists()


def test_configure_logging_with_custom_format():
    """Test configure_logging with custom format."""
    config = CliConfig(log_format="%(levelname)s: %(message)s")
    logger = configure_logging(config)

    assert logger is not None


def test_get_logger():
    """Test get_logger function."""
    logger = get_logger("test_logger")

    assert logger is not None
    assert logger.name == "test_logger"


def test_get_logger_with_config():
    """Test get_logger with config."""
    config = CliConfig(verbose=1)
    logger = get_logger("test_logger", config)

    assert logger is not None


def test_logging_context_enter_exit():
    """Test LoggingContext enter and exit."""
    config = CliConfig(verbose=1)
    original_logger = logging.getLogger("test")

    original_level = original_logger.level

    with LoggingContext(config, "test") as logger:
        assert logger is not None

    assert logging.getLogger("test").level == original_level


def test_logging_context_restores_handlers():
    """Test LoggingContext restores handlers on exit."""
    config = CliConfig(verbose=1)
    test_logger = logging.getLogger("test_context_handlers")

    original_handlers = test_logger.handlers.copy()

    with LoggingContext(config, "test_context_handlers"):
        pass

    assert len(test_logger.handlers) == len(original_handlers)


def test_logging_context_restores_handlers_with_exception():
    """Test LoggingContext restores handlers even with exception."""
    config = CliConfig(verbose=1)
    test_logger = logging.getLogger("test_context_exception")

    original_handlers = test_logger.handlers.copy()

    try:
        with LoggingContext(config, "test_context_exception"):
            raise ValueError("Test exception")
    except ValueError:
        pass

    assert len(test_logger.handlers) == len(original_handlers)


def test_configure_logging_with_logger_name():
    """Test configure_logging with specific logger name."""
    config = CliConfig(verbose=1)
    logger = configure_logging(config, "my_app")

    assert logger is not None
    assert logger.name == "my_app"
