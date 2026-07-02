"""Plugin manager."""

from .base import Plugin
from .exceptions import PluginValidationError
from .registry import PluginRegistry


class PluginManager:
    """Manages Kraken plugins."""

    def __init__(self) -> None:
        self.registry = PluginRegistry()

    def register(self, plugin: Plugin) -> None:
        """Register a plugin."""
        self.registry.register(plugin)

    def plugins(self) -> list[str]:
        """Return registered plugin names."""
        return self.registry.list()

    def validate(self) -> None:
        """Validate all registered plugins."""
        for name in self.plugins():
            plugin = self.registry.get(name)

            if plugin is None:
                continue

            if not plugin.validate():
                raise PluginValidationError(
                    f"Plugin '{name}' failed validation."
                )