"""Logging configuration utilities."""

import logging
import sys
from pathlib import Path

from cliparse.config import CliConfig


def configure_logging(
    config: CliConfig,
    logger_name: str | None = None,
) -> logging.Logger:
    """Configure logging based on CliConfig.

    Args:
        config: CLI configuration.
        logger_name: Name for the root logger (default: None for root logger).

    Returns:
        Configured logger instance.
    """
    logger = logging.getLogger(logger_name)

    log_level = config.effective_log_level
    logger.setLevel(log_level)

    handlers: list[logging.Handler] = []

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)

    formatter = logging.Formatter(
        fmt=config.log_format,
        datefmt=config.log_date_format,
    )
    console_handler.setFormatter(formatter)
    handlers.append(console_handler)

    if config.log_file:
        log_path = Path(config.log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)

        file_handler = logging.FileHandler(log_path)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        handlers.append(file_handler)

    logger.handlers.clear()
    for handler in handlers:
        logger.addHandler(handler)

    return logger


def get_logger(
    name: str,
    config: CliConfig | None = None,
) -> logging.Logger:
    """Get a logger with optional configuration.

    Args:
        name: Logger name (typically __name__).
        config: Optional CLI configuration to apply.

    Returns:
        Logger instance.
    """
    logger = logging.getLogger(name)

    if config:
        logger.setLevel(config.effective_log_level)

    return logger


class LoggingContext:
    """Context manager for temporary logging configuration.

    Example:
        with LoggingContext(CliConfig(verbose=1)):
            logger.info("This will be logged at INFO level")
    """

    def __init__(self, config: CliConfig, logger_name: str | None = None) -> None:
        """Initialize the context manager.

        Args:
            config: CLI configuration to apply.
            logger_name: Name for the logger (default: root logger).
        """
        self.config = config
        self.logger_name = logger_name
        self.logger = logging.getLogger(logger_name)
        self.previous_level = self.logger.level
        self.previous_handlers = self.logger.handlers.copy()

    def __enter__(self) -> logging.Logger:
        """Configure logging on entry.

        Returns:
            Configured logger.
        """
        configure_logging(self.config, self.logger_name)
        return self.logger

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        """Restore previous logging configuration on exit."""
        self.logger.setLevel(self.previous_level)
        self.logger.handlers.clear()
        for handler in self.previous_handlers:
            self.logger.addHandler(handler)
