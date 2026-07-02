"""Plugin-related exceptions."""


class PluginError(Exception):
    """Base exception for all plugin errors."""


class PluginRegistrationError(PluginError):
    """Raised when plugin registration fails."""


class PluginValidationError(PluginError):
    """Raised when plugin validation fails."""