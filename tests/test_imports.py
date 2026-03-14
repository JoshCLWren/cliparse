"""Tests for package imports."""


def test_import_config():
    """Test importing config module."""
    from cliparse.config import CliConfig, SubCommand

    assert CliConfig is not None
    assert SubCommand is not None


def test_import_args():
    """Test importing args module."""
    from cliparse.args import (
        ArgumentParserBuilder,
        build_parser,
        parse_args,
        run_command,
    )

    assert ArgumentParserBuilder is not None
    assert build_parser is not None
    assert parse_args is not None
    assert run_command is not None


def test_import_logging():
    """Test importing logging module."""
    from cliparse.logging import LoggingContext, configure_logging, get_logger

    assert configure_logging is not None
    assert get_logger is not None
    assert LoggingContext is not None


def test_import_from_init():
    """Test importing from package init."""
    from cliparse import (
        CliConfig,
        LoggingContext,
        SubCommand,
    )

    assert CliConfig is not None
    assert SubCommand is not None
    assert LoggingContext is not None
