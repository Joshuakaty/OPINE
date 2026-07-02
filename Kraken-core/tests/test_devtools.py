"""Unit tests for KRAKEN's developer tooling subprocess wrappers.

These tests never invoke the real `pytest`, `black`, or `ruff` processes —
`subprocess.run` is monkeypatched so the tests stay fast and hermetic, while
still verifying the exact command each wrapper constructs.
"""

from typing import Any

import pytest

from kraken import devtools


class _FakeCompletedProcess:
    """Minimal stand-in for `subprocess.CompletedProcess`."""

    def __init__(self, returncode: int) -> None:
        self.returncode = returncode


@pytest.fixture
def capture_command(monkeypatch: pytest.MonkeyPatch) -> list[list[str]]:
    """Monkeypatch `subprocess.run` to record commands instead of running them.

    Args:
        monkeypatch: The pytest fixture used to patch `subprocess.run`.

    Returns:
        A list that will be populated with each command invoked as a list
        of strings, in call order.
    """
    calls: list[list[str]] = []

    def _fake_run(command: list[str], check: bool = False, **_: Any) -> _FakeCompletedProcess:
        calls.append(list(command))
        return _FakeCompletedProcess(returncode=0)

    monkeypatch.setattr(devtools.subprocess, "run", _fake_run)
    return calls


def test_run_tests_invokes_pytest(capture_command: list[list[str]]) -> None:
    """`run_tests` should invoke pytest with no extra arguments."""
    exit_code = devtools.run_tests()

    assert exit_code == 0
    assert capture_command == [["pytest"]]


def test_run_format_invokes_black_on_target_dirs(capture_command: list[list[str]]) -> None:
    """`run_format` should invoke black against the src and tests directories."""
    exit_code = devtools.run_format()

    assert exit_code == 0
    assert capture_command == [["black", "src", "tests"]]


def test_run_format_check_appends_check_flag(capture_command: list[list[str]]) -> None:
    """`run_format(check=True)` should insert `--check` before the target dirs."""
    devtools.run_format(check=True)

    assert capture_command == [["black", "--check", "src", "tests"]]


def test_run_lint_invokes_ruff_check_on_target_dirs(capture_command: list[list[str]]) -> None:
    """`run_lint` should invoke `ruff check` against the src and tests directories."""
    exit_code = devtools.run_lint()

    assert exit_code == 0
    assert capture_command == [["ruff", "check", "src", "tests"]]


def test_run_lint_fix_appends_fix_flag(capture_command: list[list[str]]) -> None:
    """`run_lint(fix=True)` should insert `--fix` before the target dirs."""
    devtools.run_lint(fix=True)

    assert capture_command == [["ruff", "check", "--fix", "src", "tests"]]


def test_run_propagates_nonzero_exit_code(
    monkeypatch: pytest.MonkeyPatch, capture_command: list[list[str]]
) -> None:
    """A failing underlying tool should surface its exit code unchanged."""

    def _fake_run(command: list[str], check: bool = False, **_: Any) -> _FakeCompletedProcess:
        capture_command.append(list(command))
        return _FakeCompletedProcess(returncode=1)

    monkeypatch.setattr(devtools.subprocess, "run", _fake_run)

    assert devtools.run_tests() == 1
