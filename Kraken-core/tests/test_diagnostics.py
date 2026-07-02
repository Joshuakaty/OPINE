"""Unit tests for KRAKEN's `kraken doctor` diagnostic checks."""

from pathlib import Path

import pytest

from kraken.config import Settings, get_settings
from kraken.diagnostics import (
    check_log_directory,
    check_python_version,
    check_required_packages,
    check_settings_loaded,
    run_all_checks,
)


def test_check_python_version_passes_on_supported_interpreter() -> None:
    """The running test interpreter must meet KRAKEN's minimum version."""
    result = check_python_version()

    assert result.name == "Python version"
    assert result.passed is True


def test_check_required_packages_passes_when_all_importable() -> None:
    """All of KRAKEN's declared runtime dependencies should be importable."""
    result = check_required_packages()

    assert result.name == "Required packages"
    assert result.passed is True


def test_check_required_packages_fails_when_a_package_is_missing(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A missing dependency should be reported by name and fail the check."""
    monkeypatch.setattr(
        "kraken.diagnostics.REQUIRED_PACKAGES", ("definitely_not_a_real_package",)
    )

    result = check_required_packages()

    assert result.passed is False
    assert "definitely_not_a_real_package" in result.detail


def test_check_settings_loaded_reports_environment(clean_env: None) -> None:
    """The configuration check should surface the active environment."""
    settings = get_settings()

    result = check_settings_loaded(settings)

    assert result.passed is True
    assert settings.environment in result.detail


def test_check_log_directory_passes_when_file_logging_disabled(
    clean_env: None,
) -> None:
    """When file logging is off, the log directory check should pass trivially."""
    settings = Settings(log_to_file=False)

    result = check_log_directory(settings)

    assert result.passed is True
    assert "disabled" in result.detail.lower()


def test_check_log_directory_passes_when_directory_is_writable(
    clean_env: None, tmp_path: Path
) -> None:
    """A writable, configured log directory should pass the check."""
    settings = Settings(log_to_file=True, log_dir=str(tmp_path))

    result = check_log_directory(settings)

    assert result.passed is True


def test_run_all_checks_returns_one_result_per_check(clean_env: None) -> None:
    """`run_all_checks` should return a result for every individual check."""
    settings = get_settings()

    results = run_all_checks(settings)

    names = [result.name for result in results]
    assert names == [
        "Python version",
        "Required packages",
        "Configuration",
        "Log directory",
    ]
