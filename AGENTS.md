# Repository Guidelines

## Project Structure & Module Organization
The cliparse package code lives in the `cliparse` directory. The main modules are:
- `cliparse/__init__.py` - Public API exports
- `cliparse/args.py` - ArgumentParserBuilder and related utilities
- `cliparse/config.py` - CliConfig dataclass
- `cliparse/logging.py` - Logging configuration and utilities

Tooling metadata (`pyproject.toml`, `uv.lock`) defines project dependencies. Tests are in the `tests/` directory.

## Build, Test, and Development Commands
- `source .venv/bin/activate`: activate the virtual environment (do this once per session)
- `uv sync --all-extras`: install dependencies via uv
- `pytest`: run tests
- `make pytest`: run the test suite with coverage
- `make lint`: run ruff and pyright

## Getting Started
When contributing to cliparse:
1. Run `uv sync --all-extras` to install all dependencies
2. Run `source .venv/bin/activate` to activate the virtual environment
3. Run `pytest` to ensure tests pass
4. Start making changes!

## Git Worktrees (Parallel Work)
Use git worktrees to work on multiple cards in parallel without branch conflicts:
- Create a branch per card: `git switch -c card/short-slug`
- Add a worktree: `git worktree add ../cliparse-<slug> card/short-slug`
- Work only in that worktree for the card; run tests there
- Keep the branch updated: `git fetch` then `git rebase origin/main` (or merge)
- When merged, remove it: `git worktree remove ../cliparse-<slug>`
- Clean stale refs: `git worktree prune`
- WIP limit: 3 cards total in progress across all worktrees

## Test Coverage Requirements
- Current target: 96% coverage threshold (configured in `pyproject.toml`)
- Always run `pytest --cov=cliparse --cov-report=term-missing` to check missing coverage
- When touching logic or input handling, ensure tests are added to maintain coverage
- Strategies for increasing coverage:
  - Add tests for remaining uncovered edge cases
  - Add tests for complex error handling paths
  - Add tests for platform-specific code paths

## Coding Style & Naming Conventions
Follow standard PEP 8 spacing (4 spaces, 100-character soft wrap) and favor descriptive snake_case for functions and variables. Use dataclasses for typed data containers and keep public functions annotated with precise types. Prefer explicit helper names and guard callbacks with early returns rather than nesting.

Ruff configuration (from `pyproject.toml`):
- Line length: 100 characters
- Python version: 3.13
- Enabled rules: E, F, I, N, UP, B, C4, D, ANN401
- Ignored: D203, D213, E501
- Code comments are discouraged - prefer clear code and commit messages

## Pre-commit Hook
A pre-commit hook is installed in `.git/hooks/pre-commit` that automatically runs:
- Check for type/linter ignores in staged files
- Run the shared lint script (`scripts/lint.sh`)

The lint script runs:
- Python compilation check
- Ruff linting
- Any type usage check (ruff ANN401 rule)
- Pyright type checking

The hook will block commits containing `# type: ignore`, `# noqa`, `# ruff: ignore`, or `# pylint: ignore`.

To test the hook manually: `make githook` or `bash scripts/lint.sh`

## Code Quality Standards
- Run linting after each change:
  - `make lint` or `bash scripts/lint.sh`
- Use specific types instead of `Any` in type annotations (ruff ANN401 rule)
- Run tests when you touch logic or input handling:
  - `pytest`
- Always write a regression test when fixing a bug
- If you break something while fixing it, fix both in the same PR
- Do not use in-line comments to disable linting or type checks
- Do not narrate your code with comments; prefer clear code and commit messages

## Style Guidelines
- Keep helpers explicit and descriptive (snake_case), and annotate public
  functions with precise types
- Avoid shell-specific shortcuts; prefer Python APIs and `pathlib.Path` helpers
- Use the standard library only - cliparse has zero external dependencies

## Branch Workflow
- Always create a feature branch from `main` before making changes:
  - `git checkout -b feature-name`
  - Use descriptive names like `fix-bug` or `add-feature`
- Push the feature branch to create a pull request
- After your PR is merged, update your local `main`:
  - `git checkout main`
  - `git pull`
  - Delete the merged branch: `git branch -d feature-name`

## Testing Guidelines
- Automated tests live in `tests/` and run with `python -m pytest` (or `make pytest`)
- When adding tests, keep `pytest` naming like `test_example_function`
- Always use appropriate fixtures from `conftest.py` for testing dependencies
- Test files should mirror the module structure:
  - `tests/test_args.py` - tests for `cliparse/args.py`
  - `tests/test_config.py` - tests for `cliparse/config.py`
  - `tests/test_logging.py` - tests for `cliparse/logging.py`

## Commit & Pull Request Guidelines
- Use imperative, component-scoped commit messages (e.g., "Add feature X")
- Bundle related changes per commit
- PR summary should describe user impact and testing performed
- Attach screenshots when UI is affected

## cliparse-Specific Guidelines
- Keep the API simple and focused on CLI argument parsing and logging
- Avoid adding features that are better handled by other libraries (e.g., config file parsing)
- Maintain zero external dependencies - use only Python standard library
- Ensure all public APIs are exported through `cliparse/__init__.py`
- Test both the builder pattern and direct usage patterns
