"""Plugin registry."""

from .base import Plugin
from .exceptions import PluginRegistrationError


class PluginRegistry:
    """Stores registered plugins."""

    def __init__(self) -> None:
        self._plugins: dict[str, Plugin] = {}

    def register(self, plugin: Plugin) -> None:
        if plugin.name in self._plugins:
            raise PluginRegistrationError(
                f"Plugin '{plugin.name}' is already registered."
            )

        self._plugins[plugin.name] = plugin

    def get(self, name: str) -> Plugin | None:
        return self._plugins.get(name)

    def list(self) -> list[str]:
        return sorted(self._plugins.keys())