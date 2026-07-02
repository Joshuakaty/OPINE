"""Centralized logging configuration for KRAKEN, using Loguru.

Logging is configured exactly once, at the composition root (`main.py`),
and every other module simply imports `loguru.logger` to emit log records.
This module owns *how* logs are formatted and where they go; it does not
emit any log records itself.
"""

import sys

from loguru import logger

from .config import Settings
from .constants import LOG_FILE_NAME, LOG_RETENTION, LOG_ROTATION

# Console log format: timestamp, level, module:function:line, message.
_CONSOLE_FORMAT = (
    "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
    "<level>{level: <8}</level> | "
    "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
    "<level>{message}</level>"
)

# File log format mirrors the console format without color tags.
_FILE_FORMAT = (
    "{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}"
)


def configure_logging(settings: Settings) -> None:
    """Configure Loguru sinks based on validated application settings.

    Removes any existing sinks (including Loguru's default) and installs a
    console sink, plus an optional rotating file sink, according to the
    provided settings. Safe to call multiple times; each call fully resets
    the logging configuration.

    Args:
        settings: The validated application settings controlling log level,
            log directory, and whether file logging is enabled.
    """
    # Start from a clean slate so repeated calls don't duplicate sinks.
    logger.remove()

    # Console sink: always enabled, human-readable and colorized.
    logger.add(
        sys.stderr,
        level=settings.log_level,
        format=_CONSOLE_FORMAT,
        colorize=True,
        backtrace=False,
        diagnose=False,
    )

    # Optional file sink: rotating, retained per LOG_RETENTION, no ANSI color.
    if settings.log_to_file:
        settings.log_dir_path.mkdir(parents=True, exist_ok=True)
        log_file_path = settings.log_dir_path / LOG_FILE_NAME
        logger.add(
            log_file_path,
            level=settings.log_level,
            format=_FILE_FORMAT,
            rotation=LOG_ROTATION,
            retention=LOG_RETENTION,
            colorize=False,
            backtrace=False,
            diagnose=False,
        )

    logger.debug(
        "Logging configured (environment={}, level={}, file_logging={})",
        settings.environment,
        settings.log_level,
        settings.log_to_file,
    )
