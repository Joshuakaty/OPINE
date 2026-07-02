"""Base plugin interface."""

from abc import ABC, abstractmethod


class Plugin(ABC):
    """Base class for all Kraken plugins."""

    name: str = ""
    version: str = "1.0.0"

    @abstractmethod
    def collect(self):
        """Collect data."""
        raise NotImplementedError

    @abstractmethod
    def validate(self) -> bool:
        """Validate the plugin."""
        raise NotImplementedError