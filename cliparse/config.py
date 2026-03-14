"""CLI configuration dataclass."""

from dataclasses import dataclass, field


@dataclass(frozen=True)
class CliConfig:
    """Configuration for CLI applications.

    Attributes:
        verbose: Enable verbose output (can be incremented for more verbosity).
        quiet: Suppress non-error output.
        log_level: Explicit log level (overrides verbose/quiet).
        log_file: Path to log file (optional).
        log_format: Log message format.
        log_date_format: Log date format.
    """

    verbose: int = 0
    quiet: bool = False
    log_level: str | None = None
    log_file: str | None = None
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    log_date_format: str = "%Y-%m-%d %H:%M:%S"

    @property
    def effective_log_level(self) -> int:
        """Calculate effective log level from verbose/quiet settings.

        Returns:
            Logging level constant (e.g., logging.INFO, logging.DEBUG).
        """
        import logging

        if self.log_level:
            level_name = self.log_level.upper()
            level_map = {
                "DEBUG": logging.DEBUG,
                "INFO": logging.INFO,
                "WARNING": logging.WARNING,
                "ERROR": logging.ERROR,
                "CRITICAL": logging.CRITICAL,
            }
            return level_map.get(level_name, logging.INFO)

        if self.quiet:
            return logging.WARNING

        if self.verbose >= 2:
            return logging.DEBUG
        if self.verbose == 1:
            return logging.INFO

        return logging.INFO


@dataclass(frozen=True)
class SubCommand:
    """Subcommand configuration for argparse.

    Attributes:
        name: Subcommand name.
        help_text: Help text for the subcommand.
        description: Longer description for the subcommand.
    """

    name: str
    help_text: str
    description: str | None = None
    aliases: list[str] = field(default_factory=list)
