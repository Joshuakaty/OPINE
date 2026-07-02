"""Environment-based configuration loading and validation for KRAKEN.

All configuration is sourced exclusively from environment variables (via a
local `.env` file in development, loaded with python-dotenv). No secrets or
environment-specific values are ever hardcoded. See SECURITY.md for the
full policy.

Settings are validated eagerly with Pydantic so that misconfiguration fails
fast, with a clear error, rather than causing confusing behavior later.
"""

from functools import lru_cache
from pathlib import Path

from dotenv import load_dotenv
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from .constants import (
    DEFAULT_ENVIRONMENT,
    DEFAULT_LOG_DIR,
    DEFAULT_LOG_LEVEL,
    VALID_ENVIRONMENTS,
    VALID_LOG_LEVELS,
)


class Settings(BaseSettings):
    """Validated application settings sourced from environment variables.

    Each field maps to an environment variable via the `KRAKEN_` prefix
    (e.g. `KRAKEN_ENV` -> `environment`). Defaults are safe for local
    development and never point at a production resource.
    """

    model_config = SettingsConfigDict(
        env_prefix="KRAKEN_",
        case_sensitive=False,
        extra="ignore",
    )

    # Deployment environment: local | development | staging | production.
    # Explicit alias: the field name "environment" would otherwise
    # auto-derive to "KRAKEN_ENVIRONMENT" under env_prefix, but the
    # documented and supported variable name is "KRAKEN_ENV"
    # (see .env.example / README.md).
    environment: str = Field(default=DEFAULT_ENVIRONMENT, validation_alias="KRAKEN_ENV")

    # Loguru log level: TRACE | DEBUG | INFO | WARNING | ERROR | CRITICAL.
    log_level: str = DEFAULT_LOG_LEVEL

    # Directory where log files are written if file logging is enabled.
    log_dir: str = DEFAULT_LOG_DIR

    # Whether to write logs to a file in addition to stderr.
    log_to_file: bool = False

    @field_validator("environment")
    @classmethod
    def validate_environment(cls, value: str) -> str:
        """Ensure the configured environment is one KRAKEN recognizes.

        Args:
            value: The raw environment string from the environment variable.

        Returns:
            The validated, lowercased environment string.

        Raises:
            ValueError: If the value is not one of VALID_ENVIRONMENTS.
        """
        normalized = value.strip().lower()
        if normalized not in VALID_ENVIRONMENTS:
            allowed = ", ".join(VALID_ENVIRONMENTS)
            raise ValueError(f"Invalid KRAKEN_ENV '{value}'. Must be one of: {allowed}")
        return normalized

    @field_validator("log_level")
    @classmethod
    def validate_log_level(cls, value: str) -> str:
        """Ensure the configured log level is a valid Loguru level.

        Args:
            value: The raw log level string from the environment variable.

        Returns:
            The validated, uppercased log level string.

        Raises:
            ValueError: If the value is not one of VALID_LOG_LEVELS.
        """
        normalized = value.strip().upper()
        if normalized not in VALID_LOG_LEVELS:
            allowed = ", ".join(VALID_LOG_LEVELS)
            raise ValueError(f"Invalid KRAKEN_LOG_LEVEL '{value}'. Must be one of: {allowed}")
        return normalized

    @property
    def log_dir_path(self) -> Path:
        """Return the configured log directory as a resolved Path.

        Returns:
            A `Path` object pointing at the configured log directory.
        """
        return Path(self.log_dir).resolve()

    @property
    def is_production(self) -> bool:
        """Return whether the application is running in production.

        Returns:
            True if `environment` is "production", otherwise False.
        """
        return self.environment == "production"


def _load_dotenv_file() -> None:
    """Load variables from a local `.env` file into the process environment.

    This is a no-op if no `.env` file is present, which is expected in
    environments (CI, containers) where variables are injected directly.
    """
    load_dotenv(dotenv_path=Path.cwd() / ".env", override=False)


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Load, validate, and cache the application settings.

    Settings are cached for the lifetime of the process so that environment
    variables are read and validated exactly once. Use this function as the
    single entry point for accessing configuration throughout the codebase.

    Returns:
        The validated, process-wide `Settings` instance.
    """
    _load_dotenv_file()
    return Settings()
