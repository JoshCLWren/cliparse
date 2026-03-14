"""CLI config boilerplate with argparse and logging integration."""

from cliparse.args import (
    ArgumentParserBuilder,
    build_parser,
    parse_args,
    run_command,
)
from cliparse.config import CliConfig, SubCommand
from cliparse.logging import LoggingContext, configure_logging, get_logger

__version__ = "0.1.0"

__all__ = [
    "CliConfig",
    "SubCommand",
    "ArgumentParserBuilder",
    "build_parser",
    "parse_args",
    "run_command",
    "configure_logging",
    "get_logger",
    "LoggingContext",
]
