"""Tests for cliparse.config module."""

import logging

from cliparse.config import CliConfig, SubCommand


def test_cli_config_defaults():
    """Test CliConfig with default values."""
    config = CliConfig()

    assert config.verbose == 0
    assert config.quiet is False
    assert config.log_level is None
    assert config.log_file is None
    assert config.effective_log_level == logging.INFO


def test_cli_config_verbose():
    """Test CliConfig verbose levels."""
    config = CliConfig(verbose=1)
    assert config.effective_log_level == logging.INFO

    config = CliConfig(verbose=2)
    assert config.effective_log_level == logging.DEBUG

    config = CliConfig(verbose=3)
    assert config.effective_log_level == logging.DEBUG


def test_cli_config_quiet():
    """Test CliConfig quiet mode."""
    config = CliConfig(quiet=True)
    assert config.effective_log_level == logging.WARNING


def test_cli_config_log_level():
    """Test CliConfig explicit log level."""
    import logging

    config = CliConfig(log_level="DEBUG")
    assert config.effective_log_level == logging.DEBUG

    config = CliConfig(log_level="WARNING")
    assert config.effective_log_level == logging.WARNING

    config = CliConfig(log_level="ERROR")
    assert config.effective_log_level == logging.ERROR


def test_cli_config_log_level_overrides_verbose():
    """Test that explicit log level overrides verbose setting."""
    import logging

    config = CliConfig(verbose=2, log_level="WARNING")
    assert config.effective_log_level == logging.WARNING


def test_cli_config_quiet_overrides_verbose():
    """Test that quiet mode overrides verbose setting."""
    config = CliConfig(verbose=2, quiet=True)
    assert config.effective_log_level == logging.WARNING


def test_sub_command():
    """Test SubCommand dataclass."""
    cmd = SubCommand(
        name="test",
        help_text="Test command",
        description="A longer description",
    )

    assert cmd.name == "test"
    assert cmd.help_text == "Test command"
    assert cmd.description == "A longer description"
    assert cmd.aliases == []


def test_sub_command_with_aliases():
    """Test SubCommand with aliases."""
    cmd = SubCommand(
        name="test",
        help_text="Test command",
        aliases=["t", "te"],
    )

    assert cmd.aliases == ["t", "te"]
