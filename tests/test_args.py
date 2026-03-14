"""Tests for cliparse.args module."""

import pytest

from cliparse.args import (
    ArgumentParserBuilder,
    build_parser,
    parse_args,
    run_command,
)
from cliparse.config import CliConfig


def test_argument_parser_builder_basic():
    """Test basic ArgumentParserBuilder."""
    builder = ArgumentParserBuilder(
        description="Test description",
        epilog="Test epilog",
        version="1.0.0",
    )

    parser = builder.build()
    args = parser.parse_args([])

    assert args is not None


def test_argument_parser_builder_version():
    """Test ArgumentParserBuilder with version."""
    builder = ArgumentParserBuilder(
        description="Test",
        version="1.0.0",
    )

    parser = builder.build()

    with pytest.raises(SystemExit):
        parser.parse_args(["--version"])


def test_argument_parser_builder_add_verbosity():
    """Test ArgumentParserBuilder with verbosity options."""
    builder = ArgumentParserBuilder(description="Test")
    builder.add_verbosity()

    parser = builder.build()
    args = parser.parse_args(["-v"])

    assert args.verbose == 1
    assert args.quiet is False


def test_argument_parser_builder_add_verbosity_multiple():
    """Test ArgumentParserBuilder with multiple verbose flags."""
    builder = ArgumentParserBuilder(description="Test")
    builder.add_verbosity()

    parser = builder.build()
    args = parser.parse_args(["-vv"])

    assert args.verbose == 2


def test_argument_parser_builder_add_quiet():
    """Test ArgumentParserBuilder with quiet flag."""
    builder = ArgumentParserBuilder(description="Test")
    builder.add_verbosity()

    parser = builder.build()
    args = parser.parse_args(["-q"])

    assert args.quiet is True


def test_argument_parser_builder_log_level():
    """Test ArgumentParserBuilder with log level."""
    builder = ArgumentParserBuilder(description="Test")
    builder.add_verbosity()

    parser = builder.build()
    args = parser.parse_args(["--log-level", "DEBUG"])

    assert args.log_level == "DEBUG"


def test_argument_parser_builder_log_file():
    """Test ArgumentParserBuilder with log file."""
    builder = ArgumentParserBuilder(description="Test")
    builder.add_log_file()

    parser = builder.build()
    args = parser.parse_args(["--log-file", "/tmp/test.log"])

    assert args.log_file == "/tmp/test.log"


def test_argument_parser_builder_subcommands():
    """Test ArgumentParserBuilder with subcommands."""
    builder = ArgumentParserBuilder(description="Test")
    builder.add_subcommands()

    sub = builder.add_subcommand("test", "Test command")

    assert sub is not None
    assert "test" in builder._subcommands


def test_argument_parser_builder_subcommand_with_aliases():
    """Test ArgumentParserBuilder with subcommand aliases."""
    builder = ArgumentParserBuilder(description="Test")
    builder.add_subcommands()

    sub = builder.add_subcommand("test", "Test command", aliases=["t", "te"])

    assert sub is not None


def test_build_parser_basic():
    """Test build_parser convenience function."""
    parser = build_parser(
        description="Test description",
        with_verbosity=True,
        with_log_file=True,
    )

    args = parser.parse_args(["-v", "--log-file", "/tmp/test.log"])

    assert args.verbose == 1
    assert args.log_file == "/tmp/test.log"


def test_parse_args():
    """Test parse_args convenience function."""
    parser = build_parser(description="Test", with_verbosity=True)

    args, config = parse_args(parser, ["-v"])

    assert args.verbose == 1
    assert config.verbose == 1
    assert isinstance(config, CliConfig)


def test_parse_args_with_log_file():
    """Test parse_args with log file."""
    parser = build_parser(description="Test", with_verbosity=True, with_log_file=True)

    args, config = parse_args(parser, ["--log-file", "/tmp/test.log"])

    assert config.log_file == "/tmp/test.log"


def test_run_command():
    """Test run_command function."""
    parser = build_parser(description="Test")
    builder = ArgumentParserBuilder(description="Test")
    builder.add_subcommands()
    builder.add_subcommand("test", "Test command")

    parser = builder.build()

    commands_called = []

    def test_handler(args):
        commands_called.append("test")

    args = parser.parse_args(["test"])
    run_command(args, {"test": test_handler})

    assert "test" in commands_called


def test_run_command_no_command():
    """Test run_command with no command specified."""
    parser = build_parser(description="Test")

    def default_handler(args):
        pass

    args = parser.parse_args([])
    run_command(args, {}, default=default_handler)

    assert True


def test_run_command_unknown_command():
    """Test run_command with unknown command."""
    import pytest

    parser = build_parser(description="Test")

    args = parser.parse_args([])

    with pytest.raises(RuntimeError, match="No command specified"):
        run_command(args, {})


def test_add_subcommand_before_add_subcommands():
    """Test add_subcommand before add_subcommands raises error."""
    import pytest

    builder = ArgumentParserBuilder(description="Test")

    with pytest.raises(RuntimeError, match="Must call add_subcommands"):
        builder.add_subcommand("test", "Test command")


def test_build_config():
    """Test build_config method."""
    builder = ArgumentParserBuilder(description="Test")
    builder.add_verbosity()
    builder.add_log_file()

    parser = builder.build()
    args = parser.parse_args(["-v", "--log-file", "/tmp/test.log"])

    config = builder.build_config(args)

    assert config.verbose == 1
    assert config.log_file == "/tmp/test.log"
    assert isinstance(config, CliConfig)
