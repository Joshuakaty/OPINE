"""Unit tests for KRAKEN's environment-based configuration loader."""

import pytest

from kraken.config import Settings, get_settings


def test_default_settings_are_valid(clean_env: None) -> None:
    """With no environment variables set, defaults should load without error."""
    settings = get_settings()

    assert settings.environment == "local"
    assert settings.log_level == "INFO"
    assert settings.log_to_file is False


def test_environment_variable_overrides_default(
    clean_env: None, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Setting KRAKEN_ENV should override the default environment value."""
    monkeypatch.setenv("KRAKEN_ENV", "staging")

    settings = get_settings()

    assert settings.environment == "staging"


def test_invalid_environment_raises_validation_error(
    clean_env: None, monkeypatch: pytest.MonkeyPatch
) -> None:
    """An unrecognized KRAKEN_ENV value should fail validation."""
    monkeypatch.setenv("KRAKEN_ENV", "not-a-real-environment")

    with pytest.raises(ValueError):
        Settings()


def test_invalid_log_level_raises_validation_error(
    clean_env: None, monkeypatch: pytest.MonkeyPatch
) -> None:
    """An unrecognized KRAKEN_LOG_LEVEL value should fail validation."""
    monkeypatch.setenv("KRAKEN_LOG_LEVEL", "NOT_A_LEVEL")

    with pytest.raises(ValueError):
        Settings()


def test_is_production_property(clean_env: None, monkeypatch: pytest.MonkeyPatch) -> None:
    """The is_production property should reflect the configured environment."""
    monkeypatch.setenv("KRAKEN_ENV", "production")

    settings = get_settings()

    assert settings.is_production is True


def test_log_level_is_normalized_to_uppercase(
    clean_env: None, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Log level values should be normalized to uppercase regardless of input case."""
    monkeypatch.setenv("KRAKEN_LOG_LEVEL", "debug")

    settings = get_settings()

    assert settings.log_level == "DEBUG"
