"""Project-wide constants for KRAKEN.

This module holds static, non-secret values shared across the codebase.
It must never contain secrets, credentials, or environment-specific values —
those belong in `config.py`, sourced from environment variables. See
SECURITY.md for the full rationale.
"""

from typing import Final

# -----------------------------------------------------------------------------
# Identity
# -----------------------------------------------------------------------------

# Human-readable application name, used in CLI output and logs.
APP_NAME: Final[str] = "KRAKEN"

# Short description of KRAKEN's purpose, shown on the welcome screen.
APP_TAGLINE: Final[str] = "Engineering foundation for OPINE (Opportunity Intelligence Engine)"

# Name of the downstream product KRAKEN exists to support.
TARGET_PRODUCT_NAME: Final[str] = "OPINE"

# -----------------------------------------------------------------------------
# Environment
# -----------------------------------------------------------------------------

# Supported values for the KRAKEN_ENV environment variable.
VALID_ENVIRONMENTS: Final[tuple[str, ...]] = (
    "local",
    "development",
    "staging",
    "production",
)

# Default environment used when KRAKEN_ENV is not set.
DEFAULT_ENVIRONMENT: Final[str] = "local"

# -----------------------------------------------------------------------------
# Logging
# -----------------------------------------------------------------------------

# Supported Loguru log levels, in ascending order of severity.
VALID_LOG_LEVELS: Final[tuple[str, ...]] = (
    "TRACE",
    "DEBUG",
    "INFO",
    "WARNING",
    "ERROR",
    "CRITICAL",
)

# Default log level used when KRAKEN_LOG_LEVEL is not set.
DEFAULT_LOG_LEVEL: Final[str] = "INFO"

# Default directory (relative to the working directory) for log files.
DEFAULT_LOG_DIR: Final[str] = "logs"

# Filename used for the rotating application log file.
LOG_FILE_NAME: Final[str] = "kraken.log"

# Log rotation policy passed to Loguru (rotate at this file size).
LOG_ROTATION: Final[str] = "10 MB"

# Log retention policy passed to Loguru (keep logs for this duration).
LOG_RETENTION: Final[str] = "14 days"

# -----------------------------------------------------------------------------
# CLI
# -----------------------------------------------------------------------------

# Name of the installed console script, used in help text.
CLI_COMMAND_NAME: Final[str] = "kraken"

# -----------------------------------------------------------------------------
# Developer tooling (Sprint 2)
# -----------------------------------------------------------------------------

# Minimum supported Python version, checked by `kraken doctor`.
MIN_PYTHON_VERSION: Final[tuple[int, int]] = (3, 13)

# Runtime dependency modules required by KRAKEN, checked by `kraken doctor`.
# Import names, not distribution/PyPI names (e.g. `pydantic_settings`, not
# `pydantic-settings`).
REQUIRED_PACKAGES: Final[tuple[str, ...]] = (
    "typer",
    "rich",
    "loguru",
    "pydantic",
    "pydantic_settings",
    "dotenv",
)

# Source and test directories operated on by `kraken format` and `kraken lint`.
DEV_TOOL_TARGET_DIRS: Final[tuple[str, ...]] = ("src", "tests")

# Base command invoked by `kraken test`.
TEST_COMMAND: Final[tuple[str, ...]] = ("pytest",)

# Base command invoked by `kraken format`.
FORMAT_COMMAND: Final[tuple[str, ...]] = ("black",)

# Flag appended by `kraken format --check`.
FORMAT_CHECK_FLAG: Final[str] = "--check"

# Base command invoked by `kraken lint`.
LINT_COMMAND: Final[tuple[str, ...]] = ("ruff", "check")

# Flag appended by `kraken lint --fix`.
LINT_FIX_FLAG: Final[str] = "--fix"

