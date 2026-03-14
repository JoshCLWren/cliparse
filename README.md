# cliparse

[![CI Status](https://github.com/JoshCLWren/cliparse/workflows/CI/badge.svg)](https://github.com/JoshCLWren/cliparse/actions)

CLI config boilerplate with argparse and logging integration for Python 3.13+ applications.

## Features

- **Python 3.13+** with type hints throughout
- **Zero external dependencies** - uses only standard library
- **CliConfig dataclass** for configuration management
- **ArgumentParserBuilder** for fluent argparse configuration
- **Logging utilities** with automatic level configuration
- **Verbosity support** (`-v`, `-vv`, `-q`, `--log-level`)
- **Subcommand support** with builder pattern
- **pytest** with 96% minimum test coverage
- **ruff** for linting and formatting
- **pyright** for static type checking

## Installation

```bash
# From GitHub
uv add git+https://github.com/JoshCLWren/cliparse.git

# Or pip
pip install git+https://github.com/JoshCLWren/cliparse.git
```

## Quick Start

```python
#!/usr/bin/env python3
"""Example CLI application using cliparse."""

from cliparse import (
    ArgumentParserBuilder,
    CliConfig,
    configure_logging,
    parse_args,
    run_command,
)


def main():
    """Main CLI entry point."""
    # Build argument parser with verbosity options
    builder = ArgumentParserBuilder(
        description="My CLI application",
        version="1.0.0",
    )
    builder.add_verbosity()
    builder.add_log_file()
    builder.add_subcommands()

    # Add subcommands
    builder.add_subcommand("hello", "Say hello")
    builder.add_subcommand("goodbye", "Say goodbye")

    parser = builder.build()

    # Parse arguments
    args, config = parse_args(parser)

    # Configure logging
    logger = configure_logging(config)
    logger.info("Starting application")

    # Run command
    def hello_handler(args):
        logger.info("Hello, World!")

    def goodbye_handler(args):
        logger.info("Goodbye, World!")

    run_command(args, {"hello": hello_handler, "goodbye": goodbye_handler})


if __name__ == "__main__":
    main()
```

## Usage

### Basic Parser with Verbosity

```python
from cliparse import build_parser, parse_args, configure_logging

parser = build_parser(description="My App", with_verbosity=True)
args, config = parse_args(parser)

logger = configure_logging(config)
logger.info("Application started")
```

### Subcommands

```python
from cliparse import ArgumentParserBuilder, run_command

builder = ArgumentParserBuilder(description="My App")
builder.add_subcommands()

builder.add_subcommand("init", "Initialize")
builder.add_subcommand("run", "Run application")

parser = builder.build()
args = parser.parse_args(["init"])

run_command(args, {"init": init_handler, "run": run_handler})
```

### CliConfig

```python
from cliparse import CliConfig, configure_logging

config = CliConfig(verbose=1, log_file="/tmp/app.log")
logger = configure_logging(config)
```

### Logging Context Manager

```python
from cliparse import CliConfig, LoggingContext

config = CliConfig(verbose=2)

with LoggingContext(config) as logger:
    logger.debug("Detailed logging enabled")
```

## Development

### Setup

```bash
# Clone repository
git clone https://github.com/JoshCLWren/cliparse.git
cd cliparse

# Install dependencies
uv sync --all-extras

# Activate venv
source .venv/bin/activate
```

### Testing

```bash
# Run tests
pytest

# Run with coverage
pytest --cov=cliparse --cov-report=html
```

### Linting

```bash
# Run all checks
make lint

# Format code
ruff format .
ruff check . --fix
```

## API Reference

### CliConfig

Configuration dataclass for CLI applications.

```python
@dataclass(frozen=True)
class CliConfig:
    verbose: int = 0
    quiet: bool = False
    log_level: str | None = None
    log_file: str | None = None
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    log_date_format: str = "%Y-%m-%d %H:%M:%S"

    @property
    def effective_log_level(self) -> int:
        """Calculate effective log level from verbose/quiet settings."""
```

### ArgumentParserBuilder

Fluent builder for creating ArgumentParser instances.

```python
class ArgumentParserBuilder:
    def __init__(self, description: str, epilog: str | None = None, version: str | None = None)
    def add_verbosity(self) -> "ArgumentParserBuilder"
    def add_log_file(self) -> "ArgumentParserBuilder"
    def add_subcommands(self, title: str = "commands") -> "ArgumentParserBuilder"
    def add_subcommand(self, name: str, help_text: str) -> argparse.ArgumentParser
    def build(self) -> argparse.ArgumentParser
    def build_config(self, args: argparse.Namespace) -> CliConfig
```

### Logging Functions

```python
def configure_logging(config: CliConfig, logger_name: str | None = None) -> logging.Logger
def get_logger(name: str, config: CliConfig | None = None) -> logging.Logger

class LoggingContext:
    """Context manager for temporary logging configuration."""
```

### Convenience Functions

```python
def build_parser(description: str, with_verbosity: bool = True, with_log_file: bool = False) -> argparse.ArgumentParser
def parse_args(parser: argparse.ArgumentParser, args: list[str] | None = None) -> tuple[argparse.Namespace, CliConfig]
def run_command(args: argparse.Namespace, command_map: dict[str, Callable], default: Callable | None = None) -> None
```

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make changes and ensure tests pass: `pytest`
4. Run linting: `make lint`
5. Commit with conventional commits
6. Push and create a pull request

## License

MIT License - see LICENSE file for details.

## Credits

Created by Josh Wren

## Related

- [uv Documentation](https://docs.astral.sh/uv/)
- [pytest Documentation](https://docs.pytest.org/)
- [ruff Documentation](https://docs.astral.sh/ruff/)
- [pyright Documentation](https://microsoft.github.io/pyright/)
