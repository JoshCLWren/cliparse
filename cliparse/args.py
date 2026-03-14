"""Argument parser builder with common CLI options."""

import argparse
from collections.abc import Callable

from cliparse.config import CliConfig


class ArgumentParserBuilder:
    """Builder for creating ArgumentParser with common options."""

    def __init__(
        self,
        description: str,
        epilog: str | None = None,
        version: str | None = None,
    ) -> None:
        """Initialize the builder.

        Args:
            description: Description for the argument parser.
            epilog: Epilog text for help output.
            version: Version string for --version flag.
        """
        self.parser = argparse.ArgumentParser(
            description=description,
            epilog=epilog,
            formatter_class=argparse.RawDescriptionHelpFormatter,
        )
        self.subparsers = None
        self._subcommands: dict[str, argparse.ArgumentParser] = {}

        if version:
            self.parser.add_argument(
                "--version",
                action="version",
                version=version,
            )

    def add_verbosity(self) -> "ArgumentParserBuilder":
        """Add -v, -q, and --log-level options.

        Returns:
            Self for method chaining.
        """
        self.parser.add_argument(
            "-v",
            "--verbose",
            action="count",
            default=0,
            help="Increase verbosity (can be used multiple times: -v, -vv)",
        )
        self.parser.add_argument(
            "-q",
            "--quiet",
            action="store_true",
            help="Suppress non-error output",
        )
        self.parser.add_argument(
            "--log-level",
            type=str,
            choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
            help="Set explicit log level (overrides -v/-q)",
        )
        return self

    def add_log_file(self) -> "ArgumentParserBuilder":
        """Add --log-file option.

        Returns:
            Self for method chaining.
        """
        self.parser.add_argument(
            "--log-file",
            type=str,
            help="Path to log file",
        )
        return self

    def add_subcommands(
        self,
        title: str = "commands",
        help_text: str = "Available commands",
        dest: str = "command",
    ) -> "ArgumentParserBuilder":
        """Add subcommands to the parser.

        Args:
            title: Title for subcommands section.
            help_text: Help text for subcommands section.
            dest: Destination attribute name.

        Returns:
            Self for method chaining.
        """
        self.subparsers = self.parser.add_subparsers(
            title=title,
            help=help_text,
            dest=dest,
        )
        return self

    def add_subcommand(
        self,
        name: str,
        help_text: str,
        description: str | None = None,
        aliases: list[str] | None = None,
    ) -> argparse.ArgumentParser:
        """Add a subcommand to the parser.

        Must call add_subcommands() first.

        Args:
            name: Subcommand name.
            help_text: Help text for the subcommand.
            description: Longer description for the subcommand.
            aliases: Alternative names for the subcommand.

        Returns:
            The subparser for this subcommand.
        """
        if self.subparsers is None:
            msg = "Must call add_subcommands() before add_subcommand()"
            raise RuntimeError(msg)

        subparser = self.subparsers.add_parser(
            name,
            help=help_text,
            description=description,
            aliases=aliases or [],
        )
        self._subcommands[name] = subparser
        return subparser

    def build(self) -> argparse.ArgumentParser:
        """Build the argument parser.

        Returns:
            Configured ArgumentParser instance.
        """
        return self.parser

    def build_config(self, args: argparse.Namespace) -> CliConfig:
        """Build CliConfig from parsed arguments.

        Args:
            args: Parsed command-line arguments.

        Returns:
            CliConfig instance.
        """
        log_level = getattr(args, "log_level", None)
        log_file = getattr(args, "log_file", None)

        return CliConfig(
            verbose=getattr(args, "verbose", 0),
            quiet=getattr(args, "quiet", False),
            log_level=log_level,
            log_file=log_file,
        )


def build_parser(
    description: str,
    epilog: str | None = None,
    version: str | None = None,
    with_verbosity: bool = True,
    with_log_file: bool = False,
) -> argparse.ArgumentParser:
    """Convenience function to build a basic parser.

    Args:
        description: Description for the argument parser.
        epilog: Epilog text for help output.
        version: Version string for --version flag.
        with_verbosity: Whether to add -v/-q/--log-level options.
        with_log_file: Whether to add --log-file option.

    Returns:
        Configured ArgumentParser instance.
    """
    builder = ArgumentParserBuilder(description, epilog, version)

    if with_verbosity:
        builder.add_verbosity()

    if with_log_file:
        builder.add_log_file()

    return builder.build()


def parse_args(
    parser: argparse.ArgumentParser,
    args: list[str] | None = None,
) -> tuple[argparse.Namespace, CliConfig]:
    """Parse arguments and return namespace and config.

    Args:
        parser: ArgumentParser instance.
        args: Arguments to parse (default: sys.argv[1:]).

    Returns:
        Tuple of (parsed namespace, CliConfig).
    """
    parsed = parser.parse_args(args)

    config = CliConfig(
        verbose=getattr(parsed, "verbose", 0),
        quiet=getattr(parsed, "quiet", False),
        log_level=getattr(parsed, "log_level", None),
        log_file=getattr(parsed, "log_file", None),
    )

    return parsed, config


def run_command(
    args: argparse.Namespace,
    command_map: dict[str, Callable[..., None]],
    default: Callable[[argparse.Namespace], None] | None = None,
) -> None:
    """Run a command function based on parsed arguments.

    Args:
        args: Parsed command-line arguments.
        command_map: Mapping of command names to handler functions.
        default: Default handler if no command specified (e.g., parser.print_help).
    """
    command = getattr(args, "command", None)

    if command and command in command_map:
        handler = command_map[command]
        handler(args)
    elif default:
        default(args)
    else:
        msg = "No command specified"
        raise RuntimeError(msg)
