"""Environment and configuration snapshot for the `kraken info` command.

This module gathers descriptive facts about the running KRAKEN installation
and its active configuration into plain data. It performs no console I/O
itself — rendering is the job of `kraken/console/info.py`, following the
same separation of concerns used by `console/welcome.py`.
"""

import platform
from dataclasses import dataclass

from .__version__ import __version__
from .config import Settings
from .constants import APP_NAME, CLI_COMMAND_NAME, TARGET_PRODUCT_NAME


@dataclass(frozen=True)
class InfoSnapshot:
    """A point-in-time snapshot of KRAKEN's runtime and configuration state.

    Attributes:
        app_name: KRAKEN's human-readable application name.
        version: The installed KRAKEN package version.
        target_product: The downstream product KRAKEN exists to support.
        cli_command: The name of the installed console script.
        python_version: The running Python interpreter's version string.
        platform_description: A human-readable description of the host
            platform (OS, release, architecture).
        environment: The active KRAKEN deployment environment.
        log_level: The configured Loguru log level.
        log_to_file: Whether file logging is enabled.
        log_dir: The resolved log directory path, as a string.
    """

    app_name: str
    version: str
    target_product: str
    cli_command: str
    python_version: str
    platform_description: str
    environment: str
    log_level: str
    log_to_file: bool
    log_dir: str


def gather_info(settings: Settings) -> InfoSnapshot:
    """Collect a snapshot of KRAKEN's current runtime and configuration.

    Args:
        settings: The already-loaded, validated `Settings` instance.

    Returns:
        An `InfoSnapshot` describing the current installation.
    """
    return InfoSnapshot(
        app_name=APP_NAME,
        version=__version__,
        target_product=TARGET_PRODUCT_NAME,
        cli_command=CLI_COMMAND_NAME,
        python_version=platform.python_version(),
        platform_description=platform.platform(),
        environment=settings.environment,
        log_level=settings.log_level,
        log_to_file=settings.log_to_file,
        log_dir=str(settings.log_dir_path),
    )
