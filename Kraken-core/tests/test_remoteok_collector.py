"""Tests for the RemoteOK collector."""

from kraken.collectors.remoteok import RemoteOKCollector


def test_remoteok_collector_instantiates() -> None:
    collector = RemoteOKCollector()

    assert collector is not None
    assert collector.API_URL == "https://remoteok.com/api"