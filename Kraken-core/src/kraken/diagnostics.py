"""Environment diagnostic checks for the `kraken doctor` command.

This module contains pure diagnostic logic: it inspects the running Python
interpreter, KRAKEN's required dependencies, and its loaded configuration,
then reports what it finds as plain data. It performs no console I/O
itself — rendering is the job of `kraken/console/doctor.py`, following the
same separation of concerns used by `console/welcome.py`.
"""

import importlib
import sys
from dataclasses import dataclass

from .config import Settings
from .constants import MIN_PYTHON_VERSION, REQUIRED_PACKAGES


@dataclass(frozen=True)
class CheckResult:
    """The outcome of a single diagnostic check.

    Attributes:
        name: Short human-readable label for the check.
        passed: Whether the check succeeded.
        detail: Additional context shown alongside the result.
    """

    name: str
    passed: bool
    detail: str


def _is_importable(module_name: str) -> bool:
    """Return whether a module can be imported without raising.

    Args:
        module_name: The fully-qualified module name to attempt to import.

    Returns:
        True if the import succeeds, otherwise False.
    """
    try:
        importlib.import_module(module_name)
    except ImportError:
        return False
    return True


def check_python_version() -> CheckResult:
    """Verify the running interpreter meets KRAKEN's minimum version.

    Returns:
        A `CheckResult` describing the outcome.
    """
    current = (sys.version_info.major, sys.version_info.minor)
    passed = current >= MIN_PYTHON_VERSION
    detail = f"Python {sys.version_info.major}.{sys.version_info.minor} detected"
    if not passed:
        required = ".".join(str(part) for part in MIN_PYTHON_VERSION)
        detail += f" (requires >= {required})"
    return CheckResult(name="Python version", passed=passed, detail=detail)


def check_required_packages() -> CheckResult:
    """Verify that KRAKEN's required third-party packages are importable.

    Returns:
        A `CheckResult` describing the outcome, listing any missing packages.
    """
    missing = [pkg for pkg in REQUIRED_PACKAGES if not _is_importable(pkg)]
    passed = not missing
    detail = (
        "All required packages are importable"
        if passed
        else f"Missing: {', '.join(missing)}"
    )
    return CheckResult(name="Required packages", passed=passed, detail=detail)


def check_settings_loaded(settings: Settings) -> CheckResult:
    """Verify that application settings loaded and validated successfully.

    Args:
        settings: The already-loaded, validated `Settings` instance. Since
            `get_settings()` raises on invalid configuration, reaching this
            check with a `Settings` instance already proves success.

    Returns:
        A `CheckResult` describing the outcome.
    """
    detail = f"environment={settings.environment}, log_level={settings.log_level}"
    return CheckResult(name="Configuration", passed=True, detail=detail)


def check_log_directory(settings: Settings) -> CheckResult:
    """Verify that the configured log directory is writable, if enabled.

    Args:
        settings: The already-loaded, validated `Settings` instance.

    Returns:
        A `CheckResult` describing the outcome.
    """
    if not settings.log_to_file:
        return CheckResult(
            name="Log directory",
            passed=True,
            detail="File logging disabled (KRAKEN_LOG_TO_FILE=false)",
        )

    try:
        settings.log_dir_path.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        return CheckResult(
            name="Log directory",
            passed=False,
            detail=f"Not writable: {settings.log_dir_path} ({exc})",
        )

    return CheckResult(
        name="Log directory",
        passed=True,
        detail=f"Writable: {settings.log_dir_path}",
    )


def run_all_checks(settings: Settings) -> list[CheckResult]:
    """Run every diagnostic check and return their results in order.

    Args:
        settings: The already-loaded, validated `Settings` instance.

    Returns:
        A list of `CheckResult` objects, one per check.
    """
    return [
        check_python_version(),
        check_required_packages(),
        check_settings_loaded(settings),
        check_log_directory(settings),
    ]
