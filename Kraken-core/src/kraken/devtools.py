"""Subprocess wrappers around KRAKEN's developer tooling.

This module shells out to the project's existing dev dependencies (pytest,
black, ruff — see `requirements.txt` and `pyproject.toml`) so that
`kraken test`, `kraken format`, and `kraken lint` behave identically to
running those tools directly, just via a single, discoverable entry point.
It performs no console rendering itself; each tool's own output is streamed
directly to the terminal.
"""

import subprocess

from loguru import logger

from .constants import (
    DEV_TOOL_TARGET_DIRS,
    FORMAT_CHECK_FLAG,
    FORMAT_COMMAND,
    LINT_COMMAND,
    LINT_FIX_FLAG,
    TEST_COMMAND,
)


def _run(command: list[str]) -> int:
    """Run a subprocess command, streaming its output, and return its exit code.

    Args:
        command: The full command and arguments to execute.

    Returns:
        The process's exit code (0 conventionally means success).
    """
    logger.debug("Running command: {}", " ".join(command))
    result = subprocess.run(command, check=False)
    return result.returncode


def run_tests() -> int:
    """Run the project's test suite via pytest.

    Returns:
        pytest's exit code (0 means all tests passed).
    """
    return _run(list(TEST_COMMAND))


def run_format(check: bool = False) -> int:
    """Run Black over the source and test trees.

    Args:
        check: If True, only check formatting without modifying files
            (equivalent to `black --check`).

    Returns:
        Black's exit code (0 means no formatting issues).
    """
    command = list(FORMAT_COMMAND)
    if check:
        command.append(FORMAT_CHECK_FLAG)
    command.extend(DEV_TOOL_TARGET_DIRS)
    return _run(command)


def run_lint(fix: bool = False) -> int:
    """Run Ruff over the source and test trees.

    Args:
        fix: If True, automatically fix fixable lint issues
            (equivalent to `ruff check --fix`).

    Returns:
        Ruff's exit code (0 means no lint issues).
    """
    command = list(LINT_COMMAND)
    if fix:
        command.append(LINT_FIX_FLAG)
    command.extend(DEV_TOOL_TARGET_DIRS)
    return _run(command)
