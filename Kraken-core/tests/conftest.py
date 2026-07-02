"""Shared pytest fixtures for the KRAKEN test suite."""

from collections.abc import Iterator

import pytest

from kraken.config import get_settings


@pytest.fixture(autouse=True)
def _clear_settings_cache() -> Iterator[None]:
    """Ensure `get_settings()` is re-evaluated fresh for every test.

    `get_settings` is cached with `lru_cache` for production use. Tests
    that manipulate environment variables need each test to start from a
    clean cache so changes are actually picked up.

    Yields:
        None. This fixture only manages cache state around each test.
    """
    get_settings.cache_clear()
    yield
    get_settings.cache_clear()


@pytest.fixture
def clean_env(monkeypatch: pytest.MonkeyPatch) -> None:
    """Remove all KRAKEN_* environment variables before a test runs.

    Args:
        monkeypatch: The pytest fixture used to safely mutate environment
            variables for the duration of a single test.
    """
    for key in ("KRAKEN_ENV", "KRAKEN_LOG_LEVEL", "KRAKEN_LOG_DIR", "KRAKEN_LOG_TO_FILE"):
        monkeypatch.delenv(key, raising=False)
