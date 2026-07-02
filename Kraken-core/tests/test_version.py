"""Unit tests for the KRAKEN version module."""

from kraken.__version__ import __version__


def test_version_is_a_non_empty_string() -> None:
    """The package version should be exposed as a non-empty string."""
    assert isinstance(__version__, str)
    assert __version__.strip() != ""


def test_version_follows_semantic_versioning_shape() -> None:
    """The version string should have three dot-separated numeric parts."""
    parts = __version__.split(".")
    assert len(parts) == 3
    assert all(part.isdigit() for part in parts)
