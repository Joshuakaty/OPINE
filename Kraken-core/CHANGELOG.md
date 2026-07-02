# CHANGELOG

All notable changes to KRAKEN are documented in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/).

---

## [0.2.0] - Sprint 2 — Developer Productivity

### Added

- `kraken doctor` command: runs environment diagnostic checks (Python
  version, required dependencies, configuration, log directory
  writability) and reports a pass/fail table (`kraken/diagnostics.py`,
  `kraken/console/doctor.py`).
- `kraken info` command: prints a summary of KRAKEN's version, target
  product, environment, and logging configuration
  (`kraken/info.py`, `kraken/console/info.py`).
- `kraken test` command: thin wrapper around `pytest` (`kraken/devtools.py`).
- `kraken format` command: thin wrapper around `black`, with a `--check`
  flag to verify formatting without modifying files
  (`kraken/devtools.py`).
- `kraken lint` command: thin wrapper around `ruff check`, with a `--fix`
  flag to automatically apply fixable corrections (`kraken/devtools.py`).
- Unit tests for all of the above
  (`tests/test_diagnostics.py`, `tests/test_info.py`,
  `tests/test_devtools.py`, `tests/test_cli.py`).
- New developer-tooling constants in `kraken/constants.py` (minimum Python
  version, required package list, and the underlying pytest/black/ruff
  commands).

### Notes

Sprint 2 reuses Sprint 1's existing configuration (`config.py`) and logging
(`logging_config.py`) infrastructure unchanged. No product functionality
(the Opportunity Engine itself) is introduced in this release.

---

## [0.1.0] - Sprint 1 — Foundation

### Added

- Professional project structure following Clean Architecture principles.
- Governance documentation: `README.md`, `ROADMAP.md`, `ARCHITECTURE.md`,
  `SECURITY.md`, `DECISIONS.md`, `CHANGELOG.md`.
- MIT `LICENSE`.
- `.gitignore` and `.env.example`.
- Dependency and tooling configuration: `requirements.txt`,
  `pyproject.toml` (Black and Ruff configuration included).
- Application version module (`kraken/__version__.py`).
- Project-wide constants module (`kraken/constants.py`).
- Environment-based configuration loader using Pydantic and python-dotenv
  (`kraken/config.py`).
- Centralized logging configuration using Loguru
  (`kraken/logging_config.py`).
- Application entry point (`kraken/main.py`).
- CLI entry point built with Typer (`kraken/cli.py`), including `version`
  command and default welcome screen.
- Rich-rendered console welcome screen (`kraken/console/welcome.py`).
- Starter unit test suite and pytest configuration
  (`tests/conftest.py`, `tests/test_version.py`, `tests/test_config.py`).

### Notes

This release contains no product functionality. It establishes the
foundation on top of which OPINE (Opportunity Intelligence Engine) will be
built in subsequent sprints.
