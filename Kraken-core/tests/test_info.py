"""Unit tests for KRAKEN's `kraken info` snapshot logic."""

import pytest

from kraken.__version__ import __version__
from kraken.config import get_settings
from kraken.info import gather_info


def test_gather_info_reflects_current_settings(
    clean_env: None, monkeypatch: pytest.MonkeyPatch
) -> None:
    """The gathered snapshot should mirror the currently loaded settings."""
    monkeypatch.setenv("KRAKEN_ENV", "staging")
    monkeypatch.setenv("KRAKEN_LOG_LEVEL", "DEBUG")
    settings = get_settings()

    snapshot = gather_info(settings)

    assert snapshot.environment == "staging"
    assert snapshot.log_level == "DEBUG"
    assert snapshot.version == __version__


def test_gather_info_includes_runtime_details(clean_env: None) -> None:
    """The snapshot should include non-empty Python/platform details."""
    settings = get_settings()

    snapshot = gather_info(settings)

    assert snapshot.python_version.strip() != ""
    assert snapshot.platform_description.strip() != ""
    assert snapshot.app_name == "KRAKEN"
    assert snapshot.cli_command == "kraken"
