"""Tests for the Kraken plugin framework."""

from kraken.plugins import Plugin, PluginManager


class DummyPlugin(Plugin):
    name = "dummy"

    def collect(self):
        return []

    def validate(self) -> bool:
        return True


def test_plugin_registration() -> None:
    manager = PluginManager()

    manager.register(DummyPlugin())

    assert manager.plugins() == ["dummy"]