"""Single source of truth for the KRAKEN package version.

This value is read by `pyproject.toml` consumers indirectly (kept in sync
manually for Sprint 1) and by the CLI's `version` command. Keeping the
version in exactly one place avoids drift between the package metadata and
what the application reports at runtime.
"""

# Current KRAKEN version, following Semantic Versioning (https://semver.org).
# Bump this value as part of any release described in CHANGELOG.md.
__version__: str = "0.2.0"
